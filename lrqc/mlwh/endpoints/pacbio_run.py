from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from ml_warehouse.schema import PacBioRun


from lrqc.mlwh.connection import get_mlwh_db
from lrqc.mlwh.models import PacBioRunResponse, Study, Sample


router = APIRouter()


@router.get("/run", response_model=PacBioRunResponse)
def get_pacbio_run(
    run_name: str, well_label: str, db_session: Session = Depends(get_mlwh_db)
) -> PacBioRunResponse:

    stmt = select(PacBioRun).filter(
        and_(PacBioRun.well_label == well_label, PacBioRun.pac_bio_run_name == run_name)
    )

    results: List = db_session.execute(stmt).scalars().all()

    if len(results) == 0:
        raise HTTPException(404, detail="Not PacBio run found matching criteria.")
    if len(results) > 1:
        print("WARNING! THERE IS MORE THAN ONE RESULT! RETURING THE FIRST ONE")

    run: PacBioRun = results[0]

    response = PacBioRunResponse(
        run_info=run,
        metrics=run.pac_bio_product_metrics[0].pac_bio_run_well_metrics,
        study=Study(id=run.study.id_study_lims),
        sample=Sample(id=run.sample.id_sample_lims),
    )
    return response
