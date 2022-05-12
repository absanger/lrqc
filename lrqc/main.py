from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from lrqc.mlwh.models import PacBioRun
from lrqc.mlwh.run import get_run_by_name_and_label
from lrqc.mlwh.list import list_ten_recent_runs
from lrqc.mlwh.connection import session_factory
from lrqc.lrqc_outcome.router import router as lrqc_router
from lrqc.mlwh.endpoints.inbox import router as inbox_router
from lrqc.mlwh.router import router as mlwh_router


app = FastAPI(title="LRQC")
app.include_router(lrqc_router, prefix="/qc")
app.include_router(inbox_router)
app.include_router(mlwh_router, prefix="/mlwh")


def get_db():
    """Get DB connection."""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """Redirect from root to docs."""
    return RedirectResponse(url="/docs")


@app.get("/list", response_model=List[PacBioRun])
def list_ten_runs(db: Session = Depends(get_db)) -> List[PacBioRun]:
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
