from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from database import Base, SessionLocal, engine
from models import ActivityModel
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()
class Activity(BaseModel):
    problem_id: int
    title : str
    difficulty : str
    slug:str

class Problem(BaseModel):
    id:str
    title:str
    difficulty:str
    slug : str


url = "https://leetcode.com/graphql"



@app.post("/activity")
def create_activity(activity: Activity):

    db = SessionLocal()

    db_activity = ActivityModel(
        problem_id=activity.problem_id,
        title=activity.title,
        difficulty=activity.difficulty,
        slug=activity.slug
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    db.close()

    return {
        "message": "Activity saved",
        "id": db_activity.id
    }
@app.get("/")
def home():
    return {"message":"LC Presence is Running"}

@app.get("/problem/{slug}",response_model=Problem)
def get_problem(slug: str):
    query = f"""
    query {{
        question(titleSlug: "{slug}") {{
            questionId
            questionFrontendId
            title
            difficulty
            titleSlug
        }}
    }}
    """
    response = requests.post(
        url,
        json={"query": query}
    )

    data = response.json()["data"]["question"]
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Leetcode problem not found"
        )
    return {
        "id": data["questionFrontendId"],
        "title": data["title"],
        "difficulty": data["difficulty"],
        "slug": data["titleSlug"]
    }



@app.get("/problems")
def get_problems(difficulty: str = "ALL"):
    return {
        "difficulty":difficulty,
        "message": f"Showing {difficulty} problems"
    }


@app.get("/activity/latest")
def get_latest_activity():
    db = SessionLocal()

    latest_activity = (
        db.query(ActivityModel)
        .order_by(ActivityModel.id.desc())
        .first()
    )

    db.close()

    if latest_activity is None:
        raise HTTPException(
            status_code=404,
            detail="No activity found"
        )

    return {
        "id": latest_activity.id,
        "problem_id": latest_activity.problem_id,
        "title": latest_activity.title,
        "difficulty": latest_activity.difficulty,
        "slug": latest_activity.slug
    }
@app.post("/activity/from-problem/{slug}")
def save_activity_from_problem(slug: str):
    query = f"""
    query {{
        question(titleSlug: "{slug}") {{
            questionFrontendId
            title
            difficulty
            titleSlug
        }}
    }}
    """

    response = requests.post(url, json={"query": query})
    data = response.json()["data"]["question"]

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="LeetCode problem not found"
        )

    db = SessionLocal()

    db_activity = ActivityModel(
        problem_id=int(data["questionFrontendId"]),
        title=data["title"],
        difficulty=data["difficulty"],
        slug=data["titleSlug"]
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    db.close()

    return {
        "message": "Activity fetched and saved",
        "id": db_activity.id,
        "title": db_activity.title
    }
