from fastapi import APIRouter

from lrqc.mlwh.endpoints.pacbio_run import router as pacbio_run_router

router = APIRouter()
router.include_router(pacbio_run_router, prefix="/pacbio")
