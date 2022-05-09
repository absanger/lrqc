from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from lrqc.lrqc_outcome.db.db_schema import (
    Annotation as DBAnnotation,
)

from lrqc.lrqc_outcome.models import Annotation, AnnotationOut, PacBioSearch
from lrqc.lrqc_outcome.db.connection import get_lrqc_db
from lrqc.lrqc_outcome.endpoints.misc import get_or_create, get_entities_pacbio

router = APIRouter()


@router.post("/retrieve", response_model=List[AnnotationOut])
def retrieve_annotations(
    search_terms: List[PacBioSearch], db_session: Session = Depends(get_lrqc_db)
) -> List[AnnotationOut]:
    """Retrieve annotations for a list of entitiy ids"""

    entities = get_entities_pacbio(search_terms, db_session)
    output = []
    for (terms, entity) in entities:
        for db_annot in entity.annotations:
            annot = AnnotationOut(
                run_name=terms.run_name,
                well_label=terms.well_label,
                annotation=db_annot.annotation,
                user_name=db_annot.user_name,
                date_created=db_annot.date_created,
            )

            output.append(annot)

    return output


@router.post("/create")
def create_annotation(
    pacbio_entities: List[PacBioSearch],
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

    entities = [get_or_create(pacbio_ent, db_session) for pacbio_ent in pacbio_entities]

    db_annotation.entities = entities

    db_session.add(db_annotation)
    db_session.commit()
