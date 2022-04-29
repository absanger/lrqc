from typing import Dict, List
from sqlalchemy import select
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from lrqc.lrqc_outcome.db.db_schema import (
    Entity as DBEntity,
    Annotation as DBAnnotation,
)

from lrqc.lrqc_outcome.models import Annotation
from lrqc.lrqc_outcome.db.connection import get_lrqc_db

router = APIRouter()


@router.post("/retrieve", response_model=Dict[int, List[Annotation]])
def retrieve_annotations(
    entity_ids: List[int], db_session: Session = Depends(get_lrqc_db)
) -> Dict[int, List[Annotation]]:
    """Retrieve annotations for a list of entitiy ids"""

    stmt = select(DBEntity).filter(DBEntity.id_entity.in_(entity_ids))

    results = db_session.execute(stmt).scalars().all()

    output = {entity.id_entity: entity.annotations for entity in results}

    return output


@router.post("/create")
def create_annotation(
    entity_ids: List[int],
    annotation: Annotation,
    db_session: Session = Depends(get_lrqc_db),
):
    """Create an annotation for a list of entities.

    Args:
        entity_ids: list of entity IDs to annotate
        annotation: the annotation to add
        db_session: the DB session to the LRQC DB
    """

    db_annotation: DBAnnotation = annotation.to_sqlalchemy()
    entities = (
        db_session.execute(select(DBEntity).filter(DBEntity.id_entity.in_(entity_ids)))
        .scalars()
        .all()
    )

    db_annotation.entities = entities

    db_session.add(db_annotation)
    db_session.commit()
