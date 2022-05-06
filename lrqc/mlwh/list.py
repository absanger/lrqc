"""List 10 most recent runs."""

from typing import List

from ml_warehouse.schema import PacBioRunWellMetrics
from sqlalchemy import select
from sqlalchemy.orm import Session

from lrqc.mlwh.models import PacBioRun


def list_ten_recent_runs(session: Session) -> List[PacBioRun]:
    """List the ten most recent runs from pac_bio_run_well_metrics"""

    stmt = (
        select(PacBioRunWellMetrics)
        .order_by(PacBioRunWellMetrics.well_complete.desc())
        .limit(10)
    )

    return session.execute(stmt).scalars().all()
