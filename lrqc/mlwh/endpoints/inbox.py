from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from ml_warehouse.schema import PacBioRunWellMetrics
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from lrqc.mlwh.connection import get_mlwh_db
from lrqc.mlwh.models import PacBioRun

router = APIRouter()


@router.get("/inbox", response_model=List[PacBioRun])
def get_inbox(
    weeks: int, db_session: Session = Depends(get_mlwh_db)
) -> List[PacBioRun]:
    """Get inbox of PacBio runs"""

    stmt = select(PacBioRunWellMetrics).filter(
        and_(
            PacBioRunWellMetrics.polymerase_num_reads is not None,
            or_(
                and_(
                    PacBioRunWellMetrics.ccs_execution_mode.in_(
                        ("OffInstrument", "OnInstrument")
                    ),
                    PacBioRunWellMetrics.hifi_num_reads is not None,
                ),
                PacBioRunWellMetrics.ccs_execution_mode == "None",
            ),
            PacBioRunWellMetrics.well_status == "Complete",
            PacBioRunWellMetrics.well_complete.between(
                datetime.now() - timedelta(weeks=weeks), datetime.now()
            ),
        )
    )

    print(len(db_session.execute(stmt).all()))

    return db_session.execute(stmt).scalars().all()
