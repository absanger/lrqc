from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from lrqc.lrqc_outcome.models import (
    QcOutcomeOut,
    QcOutcomeInit,
    QcOutcomeOutAnnotated,
    AnnotationInit,
    PacBioSearch,
)
from lrqc.lrqc_outcome.db.db_schema import (
    QcOutcome as DBQcOutcome,
    QcOutcomeHistory as DBQcOutcomeHistory,
    QcOutcomeDict as DBQcOutcomeDict,
    Annotation as DBAnnotation,
)
from lrqc.lrqc_outcome.db.connection import get_lrqc_db
from lrqc.lrqc_outcome.endpoints.misc import get_or_create, get_entities_pacbio

router = APIRouter()


@router.post("/create")
def create_qc_outcome(
    pacbio_entity: PacBioSearch,
    qc_outcome: QcOutcomeInit,
    annotation: Optional[AnnotationInit] = None,
    db_session: Session = Depends(get_lrqc_db),
):
    """Create a QC outcome for an entity

    Args:
        pacbio_entity: run name and well label for PacBio run to create outcome for
        qc_outcome: the QC outcome to create
        annotation: optional linked annotation for the outcome
        db_session: the DB session to the LRQC DB
    """

    entity = get_or_create(pacbio_entity, db_session)

    # Check for qc_outcome
    db_qc_outcome = (
        db_session.execute(
            select(DBQcOutcome).filter(DBQcOutcome.id_entity == entity.id_entity)
        )
        .scalars()
        .all()
    )

    assert len(db_qc_outcome) <= 1
    if len(db_qc_outcome) == 1:
        # There is an existing outcome, create the historical entry
        db_qc_outcome: DBQcOutcome = db_qc_outcome[0]
        historical_outcome = DBQcOutcomeHistory(
            id_entity=db_qc_outcome.id_entity,
            id_qc_outcome_dict=db_qc_outcome.id_qc_outcome_dict,
            date_created=db_qc_outcome.date_created,
            date_updated=db_qc_outcome.date_updated,
            user_name=db_qc_outcome.user_name,
            created_by=db_qc_outcome.created_by,
        )
        db_session.add(historical_outcome)
        db_session.commit()
        db_qc_outcome.id_qc_outcome = db_qc_outcome.id_qc_outcome
    else:
        # No existing outcome, create a new one
        db_qc_outcome = DBQcOutcome(
            entity=entity,
        )

    db_qc_outcome.user_name = qc_outcome.user_name
    db_qc_outcome.created_by = qc_outcome.created_by
    db_qc_outcome.qc_outcome_dict = DBQcOutcomeDict(
        description=qc_outcome.description, long_description=qc_outcome.long_description
    )

    if annotation is not None:

        db_qc_outcome.linked_annotation = DBAnnotation(
            entities=[entity], **annotation.dict()
        )

    db_session.merge(db_qc_outcome)
    db_session.commit()


@router.post("/retrieve", response_model=List[QcOutcomeOut])
def retrieve_qc_outcomes(
    search_terms: List[PacBioSearch], db_session: Session = Depends(get_lrqc_db)
) -> List[QcOutcomeOut]:
    """Get QC outcomes for entities

    Args:
        search_terms: run_name and well_labels of the entities for which to fetch the outcomes
        db_session: DB session to the LRQC DB.

    Returns:
        a dictionary where the keys are the entity_ids and values are the QC outcomes
    """

    output = []
    entities = get_entities_pacbio(search_terms, db_session)

    for (terms, entity) in entities:
        db_qc_outcome = entity.qc_outcome
        qc_outcome = QcOutcomeOut(
            date_created=db_qc_outcome.date_created,
            date_updated=db_qc_outcome.date_updated,
            user_name=db_qc_outcome.user_name,
            created_by=db_qc_outcome.created_by,
            description=db_qc_outcome.qc_outcome_dict.description,
            long_description=db_qc_outcome.qc_outcome_dict.long_description,
            annotations=entity.annotations,
            run_name=terms.run_name,
            well_label=terms.well_label,
        )
        output.append(qc_outcome)

    return output


@router.post(
    "/retrieve_with_annotations",
    response_model=List[QcOutcomeOutAnnotated],
)
def retrieve_qc_outcome_with_annotations(
    search_terms: List[PacBioSearch], db_session: Session = Depends(get_lrqc_db)
):

    output = []

    entities = get_entities_pacbio(search_terms, db_session)

    for (terms, entity) in entities:
        if 1 == 1:
            db_qc_outcome: DBQcOutcome = entity.qc_outcome
            if db_qc_outcome is not None:
                outcome = QcOutcomeOutAnnotated(
                    date_created=db_qc_outcome.date_created,
                    date_updated=db_qc_outcome.date_updated,
                    user_name=db_qc_outcome.user_name,
                    created_by=db_qc_outcome.created_by,
                    description=db_qc_outcome.qc_outcome_dict.description,
                    long_description=db_qc_outcome.qc_outcome_dict.long_description,
                    annotations=entity.annotations,
                    run_name=terms.run_name,
                    well_label=terms.well_label,
                )
                output.append(outcome)

    return output
