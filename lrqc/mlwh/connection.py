import os
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session

config = {"DB_URL": os.environ.get("DB_URL"), "TEST": os.environ.get("LRQC_MODE")}

if config["DB_URL"] is None or config["DB_URL"] == "":
    raise Exception(
        "ENV['DB_URL'] must be set with a database URL, or LRQC_MODE must be set for testing."
    )

engine = create_engine(config["DB_URL"], future=True, echo=True)
session_factory: sessionmaker = sessionmaker(engine, expire_on_commit=False)

def get_mlwh_db() -> Session:
    """Get MLWH DB connection"""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
