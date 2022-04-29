import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = {"LQRC_DB_URL": os.environ.get("DB_URL"), "TEST": os.environ.get("LRQC_MODE")}

if config["TEST"]:
    # config["LRQC_DB_URL"] = "sqlite+pysqlite:///:memory:"
    config["LRQC_DB_URL"] = "sqlite+pysqlite:///test.db"

if config["LQRC_DB_URL"] is None or config["LQRC_DB_URL"] == "":
    raise Exception(
        "ENV['LRQC_DB_URL'] must be set with a database URL, or LRQC_MODE must be set for testing."
    )

# engine = create_engine(config["LQRC_DB_URL"])
engine = create_engine("sqlite+pysqlite:///test.db")
lrqc_session_factory: sessionmaker = sessionmaker(engine, expire_on_commit=False)


def get_lrqc_db():
    """Get LRQC DB connection."""
    db = lrqc_session_factory()
    try:
        yield db
    finally:
        db.close()
