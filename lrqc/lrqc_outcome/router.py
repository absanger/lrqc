from typing import List, Dict, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lrqc.lrqc_outcome.models import Annotation, QcOutcome
from lrqc.lrqc_outcome.db.connection import lrqc_session_factory
from lrqc.lrqc_outcome.endpoints.annotations import router as annotations_router
from lrqc.lrqc_outcome.endpoints.qc_outcomes import router as qc_outcome_router

router = APIRouter()
router.include_router(annotations_router, prefix="/annotations")
router.include_router(qc_outcome_router, prefix="/qc_outcome")
