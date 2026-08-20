from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class ActivityModel(Base):
    """A history entry for a problem opened through LeetPresence."""

    __tablename__ = "activity"

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    slug = Column(String, nullable=False)


class CurrentActivityModel(Base):
    """The one problem currently shown in Discord Rich Presence."""

    __tablename__ = "current_activity"

    id = Column(Integer, primary_key=True, default=1)
    problem_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
