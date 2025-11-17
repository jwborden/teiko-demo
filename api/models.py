from typing import Optional
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Integer,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Import(Base):
    __tablename__ = "imported"
    uid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default="gen_random_uuid()"
    )
    project: Mapped[Optional[str]] = mapped_column(String(100))
    subject: Mapped[Optional[str]] = mapped_column(String(100))
    condition: Mapped[Optional[str]] = mapped_column(String(100))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    sex: Mapped[Optional[str]] = mapped_column(String(100))
    treatment: Mapped[Optional[str]] = mapped_column(String(100))
    response: Mapped[Optional[str]] = mapped_column(String(100))
    sample: Mapped[Optional[str]] = mapped_column(String(100))
    sample_type: Mapped[Optional[str]] = mapped_column(String(100))
    time_from_treatment_start: Mapped[Optional[int]] = mapped_column(Integer)
    b_cell: Mapped[Optional[int]] = mapped_column(Integer)
    cd8_t_cell: Mapped[Optional[int]] = mapped_column(Integer)
    cd4_t_cell: Mapped[Optional[int]] = mapped_column(Integer)
    nk_cell: Mapped[Optional[int]] = mapped_column(Integer)
    monocyte: Mapped[Optional[int]] = mapped_column(Integer)


class Project(Base):
    __tablename__ = "project"
    project_id: Mapped[str] = mapped_column(String(100), primary_key=True)


class Subject(Base):
    __tablename__ = "subject"
    subject_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, CheckConstraint("age >= 0"))
    sex: Mapped[Optional[str]] = mapped_column(
        String(100), CheckConstraint("sex IN ('M', 'F', 'Other')")
    )


class Sample(Base):
    __tablename__ = "sample"
    sample_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    sample_type: Mapped[Optional[str]] = mapped_column(
        String(100), CheckConstraint("sample_type IN ('PBMC', 'WB')")
    )
    time_from_treatment_start: Mapped[Optional[int]]
    b_cell: Mapped[Optional[int]]
    cd8_t_cell: Mapped[Optional[int]]
    cd4_t_cell: Mapped[Optional[int]]
    nk_cell: Mapped[Optional[int]]
    monocyte: Mapped[Optional[int]]
    subject_id: Mapped[str] = mapped_column(
        ForeignKey("subject.subject_id"), nullable=False
    )


class SubjectCondition(Base):
    __tablename__ = "subject_condition"
    subject_id: Mapped[str] = mapped_column(
        ForeignKey("subject.subject_id"), primary_key=True
    )
    condition_name: Mapped[str] = mapped_column(String(100), primary_key=True)


class Treatment(Base):
    __tablename__ = "treatment"
    subject_id: Mapped[str] = mapped_column(
        ForeignKey("subject.subject_id"), primary_key=True
    )
    subject_condition_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    treatment_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    response: Mapped[Optional[bool]]

    __table_args__ = (
        ForeignKeyConstraint(
            ["subject_id", "subject_condition_name"],
            ["subject_condition.subject_id", "subject_condition.condition_name"],
            ondelete="CASCADE",
        ),
    )


class ProjectSubject(Base):
    __tablename__ = "project_subjects"
    project_id: Mapped[str] = mapped_column(
        ForeignKey("project.project_id"), primary_key=True
    )
    subject_id: Mapped[str] = mapped_column(
        ForeignKey("subject.subject_id"), primary_key=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id"], ["project.project_id"], ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["subject_id"], ["subject.subject_id"], ondelete="CASCADE"
        ),
    )
