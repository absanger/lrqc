from typing import List, Optional
from fastapi import FastAPI

from lrqc.db.util import PacBioRun
from lrqc.db.run import get_run_by_name_and_label
from lrqc.db.list import list_ten_recent_runs
from lrqc.db.connection import session_factory

app = FastAPI()


@app.get("/")
async def root() -> List[PacBioRun]:
    return {"message": "Hello world"}


@app.get("/list", response_model=List[PacBioRun])
async def list() -> List[PacBioRun]:
    return list_ten_recent_runs(session_factory)


@app.get("/run/{run_name}/{well_label}", response_model=Optional[PacBioRun])
async def get_run(run_name: str, well_label: str) -> Optional[PacBioRun]:
    return get_run_by_name_and_label(session_factory, run_name, well_label)
