from datetime import date
from pydantic import BaseModel, Field


class PacBioRun(BaseModel):
    pac_bio_run_name: str = Field(
        default=None,
        title="Run Name",
        description="Lims specific identifier for the pacbio run",
    )
    well_label: str = Field(
        default=None,
        title="Well Label",
        description="The well identifier for the plate, A1-H12",
    )
    well_complete: date = Field(
        default=None, title="Well Complete", description="Timestamp of well complete"
    )

    class Config:
        orm_mode = True
