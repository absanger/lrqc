from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from lrqc.db.models import PacBioRun
from lrqc.db.run import get_run_by_name_and_label
from lrqc.db.list import list_ten_recent_runs
from lrqc.db.connection import session_factory
from lrqc.lrqc_outcome.router import router as lrqc_router

app = FastAPI()
app.include_router(lrqc_router)


def get_db():
    """Get DB connection."""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/list", response_model=List[PacBioRun])
def list(db: Session = Depends(get_db)) -> List[PacBioRun]:
    """List the 10 most recent runs."""
    return list_ten_recent_runs(db)


@app.get("/run", response_model=Optional[PacBioRun])
def get_run(
    run_name: str = Query(
        ..., title="Run Name", description="Lims specific identifier for the pacbio run"
    ),
    well_label: str = Query(
        ...,
        title="Well Label",
        description="The well identifier for the plate, e.g. A1-H12",
    ),
    db: Session = Depends(get_db),
) -> Optional[PacBioRun]:
    """Get a run by run_name and well_label."""

    run = get_run_by_name_and_label(db, run_name, well_label)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found.")
    return run
