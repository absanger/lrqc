from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from lrqc.lrqc_outcome.db.db_schema import (
    Entity as DBEntity,
    Annotation as DBAnnotation,
    QcOutcome as DBQcOutcome,
)


class Entity(BaseModel):
    # id_entity: int = Field(default=None, title="primary key")
    type_: str = Field(
        default=None,
        title="Entity type",
        description="Cell, library, merged library, short string of limited length",
    )
    description_sha: str = Field(
        default=None,
        title="Description hash",
        comment="sha256 of the description string or an ordered list of description strings",
        required=True,
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
        required=True,
    )
    platform_name: str = Field(
        default=None, title="Platform name", description="Platform name, pacbio or ont"
    )

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "type_": "merged library",
                "description_sha": "07248cfa413e5e2fe3ef7384d6366ef"
                "e1b24a7e592be94c13d4ff3c43379b519",
                "description": "This is a merged library.",
            }
        }

    def to_sqlalchemy(self) -> DBEntity:
        return DBEntity(**self.dict())


class EntityOut(Entity):

    id_entity: int = Field(default=None, title="primary key")


class Annotation(BaseModel):
    # id_annotation: int = Field(default=None, title="Primary key")
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

        schema_extra = {
            "example": {
                "annotation": "This is an annotation.",
                "user_name": "ab123",
                "date_created": "2022-05-03T12:35:35.566Z",
            }
        }

    def to_sqlalchemy(self) -> DBAnnotation:
        return DBAnnotation(**self.dict())


class QcOutcomeInit(BaseModel):

    user_name: str = Field(
        default=None,
        title="User name",
        description="Real logged in user, the user running a script or an agent (a pipeline).",
    )
    created_by: str = Field(
        default=None,
        title="System which created the outcome.",
        description="Application or script name, RT ticket, etc.",
    )

    # From QcOutcomeDict
    description: str = Field(
        default=None,
        title="Short description",
        description="Short description",
    )
    long_description: str = Field(
        default=None, title="Long description", description="Long description"
    )

    class Config:
        schema_extra = {
            "example": {
                "user_name": "ab123",
                "created_by": "LRQC",
                "description": "A run.",
                "long_description": "This is a run.",
            }
        }


class QcOutcomeOut(QcOutcomeInit):

    run_name: str = Field(
        default=None, title="PacBio run name", description="PacBio run name"
    )
    well_label: str = Field(
        default=None, title="PacBio well label", description="PacBio well label"
    )
    date_created: datetime = Field(default=None, title="Date created")
    date_updated: datetime = Field(default=None, title="Date updated")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "run_name": "A1",
                "well_label": "A2",
                "date_created": "2022-05-03T12:35:35.566Z",
                "date_updated": "2022-05-03T12:35:35.566Z",
            }
            | QcOutcomeInit.Config.schema_extra["example"]
        }

    def to_sqlalchemy(self) -> DBQcOutcome:
        return DBQcOutcome(**self.dict())


class AnnotationInit(BaseModel):
    annotation: str = Field(
        default=None, title="An annotation", description="An annotation, long string."
    )
    user_name: str = Field(
        default=None,
        title="User name",
        description="Real logged in user, the user running a script or an agent (a pipeline).",
    )

    class Config:
        schema_extra = {
            "example": {
                "annotation": "This is an annotation.",
                "user_name": "ab123",
            }
        }


class PacBioSearch(BaseModel):
    run_name: str = Field(
        default=None, title="PacBio run name", description="PacBio run name"
    )
    well_label: str = Field(
        default=None, title="PacBio well label", description="PacBio well label"
    )

    class Config:
        schema_extra = {
            "example": {
                "run_name": "A1",
                "well_label": "A2",
            }
        }
        frozen = True


class QcOutcomeOutAnnotated(QcOutcomeOut):

    annotations: List[Annotation] = Field(
        default=[],
        title="Related annotations",
        description="Annotations related to the entity.",
    )

    class Config:
        schema_extra = {
            "example": QcOutcomeOut.Config.schema_extra["example"]
            | {
                "annotations": [Annotation.Config.schema_extra["example"]],
            }
        }
