from typing import List

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from lrqc.lrqc_outcome.db.db_schema import (
    Entity as DBEntity,
    PacbioEnt as PacbioEnt,
)
from lrqc.lrqc_outcome.models import PacBioSearch


def get_or_create(search_terms: PacBioSearch, db_session: Session) -> DBEntity:
    """Get an instance of DBEntity for a run_name and well_label."""

    run_name = search_terms.run_name
    well_label = search_terms.well_label

    pacbio_ent_results: List[PacbioEnt] = (
        db_session.execute(
            select(PacbioEnt).filter(
                and_(PacbioEnt.run_name == run_name, PacbioEnt.cell_label == well_label)
            )
        )
        .scalars()
        .all()
    )

    if len(pacbio_ent_results) == 1:
        pacbio_ent = pacbio_ent_results[0]

    elif len(pacbio_ent_results):
        raise Exception(
            "There should not be more than one PacbioEnt matching these search terms"
        )

    else:
        pacbio_ent = PacbioEnt(run_name=run_name, cell_label=well_label)
        pacbio_ent.entity = DBEntity(type_="cell", platform_name="pacbio")
        db_session.add(pacbio_ent)
        db_session.commit()

    return pacbio_ent.entity


def get_entities_pacbio(search_terms: List[PacBioSearch], db_session: Session):

    output = []

    for term in search_terms:
        run_name = term.run_name
        well_label = term.well_label

        results = (
            db_session.execute(
                select(PacbioEnt).filter(
                    and_(
                        PacbioEnt.run_name == run_name,
                        PacbioEnt.cell_label == well_label,
                    )
                )
            )
            .scalars()
            .all()
        )

        for r in results:
            output.append((term, r.entity))

    return output
