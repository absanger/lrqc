from datetime import date
from typing import Any, Dict, List

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


RunName = str
WellLabel = str


class InboxResults(BaseModel):

    __root__: Dict[RunName, List[WellLabel]]

    class Config:
        schema_extra = {
            "example": {
                "MY-RUN-100": ["A1", "B1", "C1"],
                "MY-RUN-101": ["A1", "B1", "D1"],
            }
        }


class Study(BaseModel):

    id: str = Field(default=None, title="Study ID.")


class Sample(BaseModel):

    id: str = Field(default=None, title="Sample ID")


class PacBioRunWellMetrics(BaseModel):

    well_start: date = Field(
        default=None, title="Well start", description="Timestamp of well start"
    )
    well_complete: date = Field(
        default=None, title="Well complete", description="Timestamp of well complete"
    )
    well_status: str = Field(
        default=None,
        title="Last recorded status",
        description="Last recorded status, primarily to explain wells not completed",
    )

    instrument_type: str = Field(default=None, title="Instrument type")
    instrument_name: str = Field(default=None, title="Instrument name")

    chip_type: str = Field(default=None, title="Chip type")

    sl_hostname: str = Field(default=None, title="SMRT Link server hostname")
    sl_hostname: str = Field(default=None, title="SMRT Link specific run uuid")

    ts_run_name: str = Field(default=None, title="The PacBio run name")

    movie_name: str = Field(default=None, title="The PacBio movie name")
    movie_minutes: int = Field(default=None, title="Movie collection time in minutes.")

    created_by: str = Field(default=None, title="SMRT Link created by user name.")

    binding_kit: str = Field(default=None, title="Binding kit version")
    sequencing_kit: str = Field(default=None, title="Binding kit version")
    sequencing_kit_lot_number: str = Field(
        default=None, title="Sequencing Kit lot number"
    )
    cell_lot_number: str = Field(default=None, title="SMRT Cell Lot Number")

    ccs_execution_mode: str = Field(
        default=None,
        title="PacBio ccs execution mode",
        description="The PacBio ccs execution mode e.g. OnInstrument, OffInstrument or None",
    )

    include_kinetics: bool = Field(
        default=None,
        title="Include kinetics",
        description="Include kinetics where ccs is run",
    )

    loading_conc: float = Field(
        default=None, title="SMRT Cell loading concentration (pM)"
    )

    run_start: date = Field(default=None, title="Timestamp of run started")
    run_complete: date = Field(default=None, title="Timestamp of run complete")
    run_status: str = Field(
        default=None,
        title="Last recorded status",
        description="Last recorded status, primarily to explain runs not completed.",
    )

    chemistry_sw_version: str = Field(
        default=None, title="PacBio chemistry software version"
    )
    instrument_sw_version: str = Field(
        default=None, title="PacBio instrument software version"
    )
    primary_analysis_sw_version: str = Field(
        default=None, title="PacBio primary analysis software version"
    )

    control_num_reads: int = Field(default=None, title="Number of control reads")
    control_concordance_mean: float = Field(
        default=None,
        title="Control concordance mean",
        description="Average concordance between the control raw reads and the control reference "
        "sequence",
    )
    control_concordance_mode: float = Field(
        default=None,
        title="Control concordance mode",
        description="The modal value from the concordance between the control raw reads and the "
        "control reference sequence",
    )
    control_read_length_mean: float = Field(
        default=None,
        title="Mean control read length",
        description="Mean polymerase read length of the control reads",
    )
    local_base_rate: float = Field(
        default=None,
        title="Average base incorporation rate",
        description="Average base incorporation rate, excluding polymerase pausing events",
    )

    polymerase_read_bases: float = Field(
        default=None,
        title="Polymerase read bases",
        description="Calculated by multiplying the number of productive (P1) WMWs by the mean "
        "polymerase read length",
    )
    polymerase_num_reads: int = Field(default=None, title="Number of polymerase reads")
    polymerase_read_length_mean: int = Field(
        default=None,
        title="Mean high-quality read length",
        description="Mean high-quality read length of all polymerase reads",
    )
    polymerase_read_length_n50: int = Field(
        default=None,
        title="Second quartile of read length",
        description="Fifty percent of the trimmed read length of all polymerase reads are longer "
        "than this value",
    )

    insert_length_mean: float = Field(
        default=None,
        title="Average subread length",
        description="Average subread length, considering only the longest subread from each ZMW",
    )
    insert_length_n50: float = Field(
        default=None,
        title="Median subread length",
        description="Fifty percent of the subreads are longer than this value when considering "
        "only the longest subread from each ZMW",
    )

    unique_molecular_bases: int = Field(
        default=None, title="Unique molecular yield in bp"
    )

    productive_zmws_num: int = Field(default=None, title="Number of productive ZMWs")
    p0_num: int = Field(
        default=None, title="Number of empty ZMWs with no high quality read detected"
    )
    p1_num: int = Field(
        default=None, title="Number of ZMWs with a high wuality read detected."
    )
    p2_num: int = Field(
        default=None,
        title="Number of other ZMWs, signal detected but no high quality read",
    )
    adapter_dimer_percent: float = Field(
        default=None,
        title="Percentage of pre-filter ZMWs which have observed inserts of 0-10 bp",
    )
    short_insert_percent: float = Field(
        default=None,
        title="Percentage of pre-filter ZMWs which have observed inserts of 11-100 bp",
    )

    hifi_read_bases: int = Field(default=None, title="Number of HiFi bases")
    hifi_num_reads: int = Field(default=None, title="Number of HiFi reads")
    hifi_read_length_mean: int = Field(default=None, title="Mean HiFi read length")
    hifi_read_quality_median: int = Field(
        default=None, title="Median HiFi base quality"
    )
    hifi_number_passes_mean: int = Field(
        default=None, title="Mean number of passes per HiFi read"
    )

    hifi_low_quality_read_bases: int = Field(
        default=None, title="Number of HiFi bases filtered due to low quality (<Q20)"
    )
    hifi_low_quality_num_reads: int = Field(
        default=None, title="Number of HiFi reads filtered due to low quality (<Q20)"
    )
    hifi_low_quality_read_length_mean: int = Field(
        default=None, title="Mean HiFi read length filtered due to low quality (<Q20)"
    )
    hifi_low_quality_read_quality_median: int = Field(
        default=None,
        title="Median HiFi base quality filtered due to low quality (<Q20)",
    )
    hifi_low_quality_number_passes_mean: int = Field(
        default=None,
        title="Mean number of passes per HiFi read filtered due to low quality (<Q20)",
    )

    class Config:

        orm_mode = True


class Well(BaseModel):

    label: str = Field(default=None, title="Well Label")
    uuid_lims: str = Field(default=None, title="LIMS label uuid")

    class Config:
        orm_mode = False


class PacBioLibraryTube(BaseModel):

    id_lims: str = Field(default=None, title="library tube LIMS id")
    uuid: str = Field(default=None, title="library tube uuid")
    name: str = Field(default=None, title="library tube name")

    class Config:
        orm_mode = False


class PacBioRunInfo(BaseModel):

    last_updated: date = Field(default=None)
    recorded_at: date = Field(default=None)
    id_pac_bio_run_lims: str = Field(default=None)
    pac_bio_run_name: str = Field(default=None)
    pipeline_id_lims: str = Field(default=None)
    cost_code: str = Field(default=None)
    well: Well
    pac_bio_library_tube: PacBioLibraryTube

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj: Any) -> "PacBioRunInfo":
        obj.well = Well(
            label=getattr(obj, "well_label", None),
            uuid_lims=getattr(obj, "well_uuid_lims", None),
        )

        obj.pac_bio_library_tube = PacBioLibraryTube(
            id_lims=getattr(obj, "pac_bio_library_tube_id_lims", None),
            uuid=getattr(obj, "pac_bio_library_tube_uuid", None),
            name=getattr(obj, "pac_bio_library_tube_name", None),
        )

        return super().from_orm(obj)


class PacBioRunResponse(BaseModel):
    run_info: PacBioRunInfo
    study: Study
    sample: Sample
    metrics: PacBioRunWellMetrics
