from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from lrqc.lrqc_outcome.models import QcOutcome
from lrqc.lrqc_outcome.db.db_schema import (
    Entity as DBEntity,
    QcOutcome as DBQcOutcome,
)
from lrqc.lrqc_outcome.db.connection import get_lrqc_db

router = APIRouter()


@router.post("/create")
def create_qc_outcome(
    qc_outcome: QcOutcome, db_session: Session = Depends(get_lrqc_db)
):
    """Create a QC outcome for an entity

    Args:
        qc_outcome: the QC outcome to create
        db_session: the DB session to the LRQC DB
    """

    db_qc_outcome: DBQcOutcome = qc_outcome.to_sqlalchemy()
    db_session.add(db_qc_outcome)
    db_session.commit()


@router.post("/retrieve", response_model=Dict[int, QcOutcome])
def retrieve_qc_outcomes(
    entity_ids: List[int], db_session: Session = Depends(get_lrqc_db)
) -> Dict[int, QcOutcome]:
    """Get QC outcomes for entities

    Args:
        entity_ids: IDs of the entities for which to fetch the outcomes
        db_session: DB session to the LRQC DB.

    Returns:
        a dictionary where the keys are the entity_ids and values are the QC outcomes
    """

    stmt = select(DBEntity).filter(DBEntity.id_entity.in_(entity_ids))

    results = db_session.execute(stmt).scalars().all()

    output = {entity.id_entity: entity.qc_outcome for entity in results}

    return output
