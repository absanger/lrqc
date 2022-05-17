from fastapi import FastAPI
from starlette.responses import RedirectResponse
from lrqc.lrqc_outcome.router import router as lrqc_router
from lrqc.mlwh.router import router as mlwh_router


app = FastAPI(title="LRQC")
app.include_router(lrqc_router, prefix="/qc")
app.include_router(mlwh_router, prefix="/mlwh")


@app.get("/")
async def root():
    """Redirect from root to docs."""
    return RedirectResponse(url="/docs")
