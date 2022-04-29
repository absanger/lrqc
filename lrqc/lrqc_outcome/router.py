from fastapi import APIRouter

from lrqc.lrqc_outcome.endpoints.annotations import router as annotations_router
from lrqc.lrqc_outcome.endpoints.qc_outcomes import router as qc_outcome_router

router = APIRouter()
router.include_router(annotations_router, prefix="/annotations")
router.include_router(qc_outcome_router, prefix="/qc_outcome")
