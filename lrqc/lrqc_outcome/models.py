from datetime import datetime
from pydantic import BaseModel, Field

from lrqc.lrqc_outcome.db.db_schema import (
    Entity as DBEntity,
    Annotation as DBAnnotation,
    QcOutcome as DBQcOutcome,
)


class Entity(BaseModel):
    id_entity: int = Field(default=None, title="primary key")
    type_: str = Field(
        default=None,
        title="Entity type",
        description="Cell, library, merged library, short string of limited length",
    )
    description_sha: str = Field(
        default=None,
        title="Description hash",
        comment="sha256 of the description string or an ordered list of description strings",
    )
    description: str = Field(
        default=None,
        title="Description string",
        description="Description string or an ordered list of description strings.",
    )
    json_: dict = Field(
        default=None,
        title="Optional JSON representation",
        description="An optional JSON representation of the entity",
    )
    platform_name: str = Field(
        default=None, title="Platform name", description="Platform name, pacbio or ont"
    )

    class Config:
        orm_mode = True

    def to_sqlalchemy(self) -> DBEntity:
        return DBEntity(**self.dict())


class Annotation(BaseModel):
    id_annotation: int = Field(default=None, title="Primary key")
    annotation: str = Field(
        default=None, title="An annotation", description="An annotation, long string."
    )
    user_name: str = Field(
        default=None,
        title="User name",
        description="Real logged in user, the user running a script or an agent (a pipeline)",
    )
    date_created: datetime = Field(
        default=None,
        title="Date and time the annotation was created.",
        description="Date and time the annotation was created.",
    )

    class Config:
        orm_mode = True

    def to_sqlalchemy(self) -> DBAnnotation:
        return DBAnnotation(**self.dict())


class QcOutcome(BaseModel):

    id_qc_outcome: int = Field(default=None, title="Primary key")
    id_entity: int = Field(default=None, title="Foreign key for entity")
    id_qc_outcome_dict: int = Field(
        default=None, title="Foreign key for qc_outcome_dict"
    )
    date_created: datetime = Field(default=None, title="Date created")
    date_updated: datetime = Field(default=None, title="Date updated")
    user_name: str = Field(
        default=None,
        title="User name",
        description="Real logged in user, the user running a script or an agent (a pipeline)",
    )
    created_by: str = Field(
        default=None,
        title="System which created the outcome.",
        description="Application or script name, RT ticket, etc.",
    )

    class Config:
        orm_mode = True

    def to_sqlalchemy(self) -> DBQcOutcome:
        return DBQcOutcome(**self.dict())
