"""Get run."""

from typing import Optional
from pytest import Session
from ml_warehouse.schema import PacBioRunWellMetrics
from sqlalchemy import select
from lrqc.mlwh.models import PacBioRun


def get_run_by_name_and_label(
    session: Session, run_name: str, well_label: str
) -> Optional[PacBioRun]:
    """Get a PacBioRun by run_name and well_label."""

    stmt = select(PacBioRunWellMetrics).filter(
        (PacBioRunWellMetrics.well_label == well_label)
        & (PacBioRunWellMetrics.pac_bio_run_name == run_name)
    )

    # pac_bio_run_name and well_label act as composite key so there is at most one result
    return session.execute(stmt).scalars().first()
