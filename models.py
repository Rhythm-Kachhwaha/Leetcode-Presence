from sqlalchemy import Column, Integer, String
from database import Base


class ActivityModel(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer)
    title = Column(String)
    difficulty = Column(String)
    slug = Column(String)
