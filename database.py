from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./leetpresence.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)
