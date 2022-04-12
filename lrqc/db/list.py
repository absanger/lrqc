"""List 10 most recent runs."""

from typing import Iterable, List

from lrqc.db.models import PacBioRun
from ml_warehouse.schema import PacBioRunWellMetrics
from sqlalchemy import select
from sqlalchemy.orm import Session


def list_ten_recent_runs(session: Session) -> List[PacBioRun]:
    """List the ten most recent runs from pac_bio_run_well_metrics"""

    stmt = (
        select(
            PacBioRunWellMetrics.pac_bio_run_name,
            PacBioRunWellMetrics.well_label,
            PacBioRunWellMetrics.well_complete,
        )
        .order_by(PacBioRunWellMetrics.well_complete.desc())
        .limit(10)
    )

    runs: Iterable[PacBioRunWellMetrics] = session.execute(stmt).all()
    output = []
    for run in runs:
        output.append(
            PacBioRun(
                name=run.pac_bio_run_name,
                well_label=run.well_label,
                well_complete=run.well_complete,
            )
        )

    return output
