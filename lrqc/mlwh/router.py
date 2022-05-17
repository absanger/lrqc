from fastapi import APIRouter

from lrqc.mlwh.endpoints.pacbio_run import router as pacbio_run_router
from lrqc.mlwh.endpoints.inbox import router as inbox_router

router = APIRouter()
router.include_router(pacbio_run_router, prefix="/pacbio")
router.include_router(inbox_router, prefix="/pacbio")
