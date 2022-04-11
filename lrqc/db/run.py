"""Get run."""

from typing import Optional
from pytest import Session
from ml_warehouse.schema import PacBioRunWellMetrics
from sqlalchemy import select
from lrqc.db.util import PacBioRun


def get_run_by_name_and_label(
    session_factory, run_name: str, well_label: str
) -> Optional[PacBioRun]:
    """Get a PacBioRun by run_name and well_label."""

    with session_factory() as session:
        session: Session

        stmt = select(
            PacBioRunWellMetrics.pac_bio_run_name,
            PacBioRunWellMetrics.well_label,
            PacBioRunWellMetrics.well_complete,
        ).filter(
            (PacBioRunWellMetrics.well_label == well_label)
            & (PacBioRunWellMetrics.pac_bio_run_name == run_name)
        )

        # pac_bio_run_name and well_label act as composite key so there is at most one result
        run: Optional[PacBioRunWellMetrics] = session.execute(stmt).first()

        if run is not None:
            return PacBioRun(
                name=run.pac_bio_run_name,
                well_label=run.well_label,
                well_complete=run.well_complete,
            )

        return None
