from sqlalchemy import JSON, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

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
        comment="sha256 of the description string (see 'pacbio_ent') or an ordered list of "
        "description strings",
    )
    description = Column(
        String(64),
        comment="Description string (see 'pacbio_ent') or an ordered list of description strings",
    )
    json_ = Column(
        JSON, nullable=True, comment="An optional JSON representation of the entity"
    )
    platform_name = Column(String(64), comment="As pacbio or ont")

    annotations = relationship(
        "Annotation", secondary="entity_annotation", back_populates="entities"
    )
    qc_outcome = relationship("QcOutcome", back_populates="entity", uselist=False)
    qc_outcome_history = relationship("QcOutcomeHistory", back_populates="entity")

    pacbio_entities = relationship(
        "PacbioEnt", secondary="entity_pacbio_ent", back_populates="entity"
    )


class PacbioEnt(Base):
    __tablename__ = "pacbio_ent"

    id_pacbio_ent = Column(Integer, primary_key=True)
    run_name = Column(String(64), comment="Traction LIMS run name")
    cell_label = Column(String(64), nullable=True, comment="PacBio cell label")
    tag1_sequence = Column(String(64), nullable=True)
    description = Column(
        String(64),
        comment="A human-readable unique string listing the four attributes in the order they are"
        " presented here.",
    )

    entity = relationship(
        "Entity",
        secondary="entity_pacbio_ent",
        back_populates="pacbio_entities",
        uselist=False,
    )


class EntityPacbioEnt(Base):
    __tablename__ = "entity_pacbio_ent"

    id_entity_pacbio_ent = Column(Integer, primary_key=True)
    id_entity = Column(
        Integer, ForeignKey("entity.id_entity"), comment="Foreign key, see entity"
    )
    id_pacbio_ent = Column(
        Integer,
        ForeignKey("pacbio_ent.id_pacbio_ent"),
        comment="Foreign key, see pacbio_ent",
    )


class QcOutcome(Base):
    __tablename__ = "qc_outcome"

    id_qc_outcome = Column(Integer, primary_key=True)
    id_entity = Column(
        Integer, ForeignKey("entity.id_entity"), comment="Foreign key, see 'entity'"
    )
    id_qc_outcome_dict = Column(
        Integer,
        ForeignKey("qc_outcome_dict.id_qc_outcome_dict"),
        comment="Foreign key, see 'qc_outcome_dict'",
    )
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_name = Column(
        String(64),
        comment="Real logged user, the user running a script or an agent (a pipeline)",
    )
    created_by = Column(
        String(64), comment="Application or script name, RT ticket, etc."
    )

    entity = relationship("Entity", back_populates="qc_outcome", uselist=False)
    qc_outcome_dict = relationship(
        "QcOutcomeDict", back_populates="qc_outcome", uselist=False
    )
    linked_annotation = relationship(
        "Annotation",
        secondary="entity_annotation",
        back_populates="linked_qc_outcome",
        uselist=False,
        overlaps="annotations",
    )


class QcOutcomeDict(Base):
    __tablename__ = "qc_outcome_dict"

    id_qc_outcome_dict = Column(Integer, primary_key=True)
    description = Column(String(64), unique=True, comment="Short description")
    long_description = Column(String(64), comment="Long description")

    qc_outcome = relationship(
        "QcOutcome", back_populates="qc_outcome_dict", uselist=False
    )
    qc_outcome_history = relationship(
        "QcOutcomeHistory", back_populates="qc_outcome_dict", uselist=False
    )


class QcOutcomeHistory(Base):
    __tablename__ = "qc_outcome_history"

    id_qc_outcome_history = Column(Integer, primary_key=True)
    # TODO: make foreign key
    id_entity = Column(
        Integer, ForeignKey("entity.id_entity"), comment="Foreign key, see entity"
    )
    # TODO: make foreign key
    id_qc_outcome_dict = Column(
        Integer,
        ForeignKey("qc_outcome_dict.id_qc_outcome_dict"),
        comment="Foreign key, see 'qc_outcome_dict'",
    )
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_name = Column(
        String(64),
        comment="Real logged user, the user running a script or an agent (a pipeline)",
    )
    created_by = Column(
        String(64), comment="Application or script name, RT ticket, etc."
    )

    entity = relationship("Entity", back_populates="qc_outcome_history", uselist=False)
    qc_outcome_dict = relationship(
        "QcOutcomeDict", back_populates="qc_outcome_history", uselist=False
    )


class Annotation(Base):
    __tablename__ = "annotation"

    id_annotation = Column(Integer, primary_key=True)
    annotation = Column(String(64), comment="Long string")
    user_name = Column(
        String(64),
        comment="Real logged user the user running a script or an agent (a pipeline)",
    )
    date_created = Column(
        DateTime,
        server_default=func.now(),
        comment="Date and time the annotation was created",
    )

    entities = relationship(
        "Entity",
        secondary="entity_annotation",
        back_populates="annotations",
        overlaps="linked_annotation",
    )
    linked_qc_outcome = relationship(
        "QcOutcome",
        secondary="entity_annotation",
        back_populates="linked_annotation",
        uselist=False,
        overlaps="annotations,entities",
    )


class EntityAnnotation(Base):
    __tablename__ = "entity_annotation"

    id_entity_annotation = Column(Integer, primary_key=True)
    id_entity = Column(
        Integer, ForeignKey("entity.id_entity"), comment="Foreign key, see 'entity'"
    )
    id_annotation = Column(
        Integer,
        ForeignKey("annotation.id_annotation"),
        comment="Foreign key, see 'annotation'",
    )
    id_qc_outcome = Column(
        Integer,
        ForeignKey("qc_outcome.id_qc_outcome"),
        nullable=True,
        comment="If defined, a foreign key, see 'qc_outcome'",
    )
