from black import json

from sqlalchemy import JSON, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Entity(Base):
    __tablename__ = "entity"

    id_entity = Column(Integer, primary_key=True)
    type_ = Column(
        String(64),
        comment="Cell, library, merged library, short string, limited length",
    )
    description_sha = Column(
        String(64),
        unique=True,
        comment="sha256 of the description string (see 'pacbio_ent) or an ordered list of description strings",
    )
    description = Column(
        String(),
        comment="Description string (see 'pacbio_ent') or an ordered list of description strings",
    )
    json_ = Column(
        JSON, nullable=True, comment="An optional JSON representation of the entity"
    )
    platform_name = Column(String(64), comment="As pacbio or ont")


class PacbioEnt(Base):
    __tablename__ = "pacbio_ent"

    id_pacbio_ent = Column(Integer, primary_key=True)
    run_name = Column(String(), comment="Traction LIMS run name")
    cell_label = Column(String(), nullable=True, comment="PacBio cell label")
    tag1_sequence = Column(String(), nullable=True)
    description = Column(
        String(),
        comment="A human-readable unique string listing the four attributes in the order they are presented here.",
    )

class EntityPacbioEnt(Base):
    __tablename__ = "entity_pacbio_ent"

    id_entity_pacbio_ent = Column(Integer, primary_key=True)
    # TODO: make foreign key
    id_entity = Column(String(), comment="Foreign key, see 'entity'")
    # TODO: make foreign key
    id_pacbio_ent = Column(String(), comment="Foreign key, see 'pacbio_ent'")

class QcOutcome(Base):
    __tablename__ = "qc_outcome"

    id_qc_outcome = Column(Integer, primary_key=True)
    # TODO: make foreign key
    id_entity = Column(Integer, comment="Foreign key, see 'entity'")
    # TODO: make foreign key
    id_qc_outcome_dict = Column(Integer, comment="Foreign key, see 'qc_outcome_dict'")
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    user_name = Column(String(), comment="Real logged user, the user running a script or an agent (a pipeline)")
    created_by = Column(String(), comment="Application or script name, RT ticket, etc.")

class QcOutcomeDict(Base):
    __tablename__ = "qc_outcome_dict"

    id_qc_outcome_dict = Column(Integer, primary_key=True)
    description = Column(String(), unique=True, comment="Short description")
    long_description = Column(String(), comment="Long description")

class QcOutcomeHistory(Base):
    __tablename__ = "qc_outcome_history"

    id_qc_outcome_history = Column(Integer, primary_key=True)
    # TODO: make foreign key
    id_entity = Column(Integer, comment="Foreign key, see 'entity'")
    # TODO: make foreign key
    id_qc_outcome_dict = Column(Integer, comment="Foreign key, see 'qc_outcome_dict'")
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    user_name = Column(String(), comment="Real logged user, the user running a script or an agent (a pipeline)")
    created_by = Column(String(), comment="Application or script name, RT ticket, etc.")

class Annotation(Base):
    __tablename__ = "annotation"

    id_annotation = Column(Integer, primary_key=True)
    annotation = Column(String(), comment="Long string")
    user_name = Column(String(), comment="Real logged userm the user running a script or an agent (a pipeline)")
    date_created = Column(DateTime, comment="Date and time the annotation was created")

class EntityAnnotation(Base):
    __tablename__ = "entity_annotation"

    id_entity_annotation = Column(Integer, primary_key=True)
    # TODO: make foreign key
    id_entity = Column(Integer, comment="Foreign key, see 'entity'")
    # TODO: make foreign key
    id_annotation = Column(Integer, comment="Foreign key, see 'annotation'")
    # TODO: make foreign key
    id_qc_outcome = Column(Integer, nullable=True, comment="If defined, a foreign key, see 'qc_outcome'")