from collections.abc import Generator

import requests
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from leetcode import fetch_problem
from models import ActivityModel, CurrentActivityModel


Base.metadata.create_all(bind=engine)
app = FastAPI(title="LeetPresence API")


class Activity(BaseModel):
    problem_id: int
    title: str
    difficulty: str
    slug: str


class Problem(BaseModel):
    id: str
    title: str
    difficulty: str
    slug: str


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def as_dict(activity: ActivityModel | CurrentActivityModel) -> dict:
    return {
        "id": activity.id,
        "problem_id": activity.problem_id,
        "title": activity.title,
        "difficulty": activity.difficulty,
        "slug": activity.slug,
    }


def save_current_activity(db: Session, activity: Activity) -> tuple[CurrentActivityModel, bool]:
    current = db.get(CurrentActivityModel, 1)
    changed = current is None or current.slug != activity.slug

    if current is None:
        current = CurrentActivityModel(id=1, **activity.model_dump())
        db.add(current)
    elif changed:
        current.problem_id = activity.problem_id
        current.title = activity.title
        current.difficulty = activity.difficulty
        current.slug = activity.slug

    if changed:
        db.add(ActivityModel(**activity.model_dump()))
        db.commit()
        db.refresh(current)

    return current, changed


@app.get("/")
def home():
    return {"message": "LeetPresence API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/activity")
def create_activity(activity: Activity, db: Session = Depends(get_db)):
    current, changed = save_current_activity(db, activity)
    return {"message": "Activity saved", "changed": changed, "activity": as_dict(current)}


@app.get("/activity/latest")
def get_latest_activity(db: Session = Depends(get_db)):
    current = db.get(CurrentActivityModel, 1)
    if current is None:
        raise HTTPException(status_code=404, detail="No current LeetCode problem")
    return as_dict(current)


@app.get("/activity/history")
def get_activity_history(limit: int = 20, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    history = db.query(ActivityModel).order_by(ActivityModel.id.desc()).limit(limit).all()
    return [as_dict(activity) for activity in history]


@app.post("/activity/clear")
def clear_current_activity(db: Session = Depends(get_db)):
    current = db.get(CurrentActivityModel, 1)
    if current is not None:
        db.delete(current)
        db.commit()
    return {"message": "Current activity cleared"}


@app.get("/problem/{slug}", response_model=Problem)
def get_problem(slug: str):
    try:
        problem = fetch_problem(slug)
    except (requests.RequestException, ValueError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    if problem is None:
        raise HTTPException(status_code=404, detail="LeetCode problem not found")

    return {
        "id": problem["questionFrontendId"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "slug": problem["titleSlug"],
    }


@app.post("/activity/from-problem/{slug}")
def save_activity_from_problem(slug: str, db: Session = Depends(get_db)):
    try:
        problem = fetch_problem(slug)
    except (requests.RequestException, ValueError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    if problem is None:
        raise HTTPException(status_code=404, detail="LeetCode problem not found")

    activity = Activity(
        problem_id=int(problem["questionFrontendId"]),
        title=problem["title"],
        difficulty=problem["difficulty"],
        slug=problem["titleSlug"],
    )
    current, changed = save_current_activity(db, activity)
    return {
        "message": "Current activity updated" if changed else "Current activity unchanged",
        "changed": changed,
        "activity": as_dict(current),
    }
