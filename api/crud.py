from typing import Optional, Sequence

from api.models import (
    Import,
    Project,
    Subject,
    Sample,
    SubjectCondition,
    Treatment,
    ProjectSubject,
)
from sqlalchemy import Row, create_engine, select, update, delete
from sqlalchemy.orm import Session


engine = create_engine(
    "postgresql+psycopg2://demo_user:password@localhost:5433/demo_db", echo=True
)
SessionLocal: Session = Session(engine)


def create_imports(import_data: list[Import]) -> None:
    with SessionLocal as db:
        db.add_all(import_data)
        db.commit()
        return None


def get_imports_by_sample_id(
    sample_ids: Optional[list[str]],
) -> Sequence[Row[tuple[Import]]]:
    with SessionLocal as db:
        stmt = select(Import)
        if sample_ids:
            stmt = stmt.where(Import.sample.in_(sample_ids))
        results = db.execute(stmt).all()
        return results


def update_import(import_record: Import) -> None:
    with SessionLocal as db:
        stmt = (
            update(Import)
            .where(Import.uid == import_record.uid)
            .values(**import_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_imports_by_sample_id(sample_ids: list[str]) -> None:
    with SessionLocal as db:
        stmt = delete(Import).where(Import.sample.in_(sample_ids))
        db.execute(stmt)
        db.commit()
        return None


def create_projects(projects: list[Project]) -> None:
    with SessionLocal as db:
        db.add_all(projects)
        db.commit()
        return None


def get_project_by_project_id(
    project_ids: Optional[list[str]] = None,
) -> Sequence[Row[tuple[Project]]]:
    with SessionLocal as db:
        stmt = select(Project)
        if project_ids:
            stmt = stmt.where(Project.project_id.in_(project_ids))
        results = db.execute(stmt).all()
        return results


def update_project(project_record: Project) -> None:
    with SessionLocal as db:
        stmt = (
            update(Project)
            .where(Project.project_id == project_record.project_id)
            .values(**project_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_projects_by_project_id(project_ids: list[str]) -> None:
    with SessionLocal as db:
        stmt = delete(Project).where(Project.project_id.in_(project_ids))
        db.execute(stmt)
        db.commit()
        return None


def create_subjects(subjects: list[Subject]) -> None:
    with SessionLocal as db:
        db.add_all(subjects)
        db.commit()
        return None


def get_subjects_by_subject_id(
    subject_ids: Optional[list[str]],
) -> Sequence[Row[tuple[Subject]]]:
    with SessionLocal as db:
        stmt = select(Subject)
        if subject_ids:
            stmt = stmt.where(Subject.subject_id.in_(subject_ids))
        results = db.execute(stmt).all()
        return results


def update_subject(subject_record: Subject) -> None:
    with SessionLocal as db:
        stmt = (
            update(Subject)
            .where(Subject.subject_id == subject_record.subject_id)
            .values(**subject_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_subjects_by_subject_id(subject_ids: list[str]) -> None:
    with SessionLocal as db:
        stmt = delete(Subject).where(Subject.subject_id.in_(subject_ids))
        db.execute(stmt)
        db.commit()
        return None


def create_samples(samples: list[Sample]) -> None:
    with SessionLocal as db:
        db.add_all(samples)
        db.commit()
        return None


def get_samples_by_sample_id(
    sample_ids: Optional[list[str]],
) -> Sequence[Row[tuple[Sample]]]:
    with SessionLocal as db:
        stmt = select(Sample)
        if sample_ids:
            stmt = stmt.where(Sample.sample_id.in_(sample_ids))
        results = db.execute(stmt).all()
        return results


def update_sample(sample_record: Sample) -> None:
    with SessionLocal as db:
        stmt = (
            update(Sample)
            .where(Sample.sample_id == sample_record.sample_id)
            .values(**sample_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_samples_by_sample_id(sample_ids: list[str]) -> None:
    with SessionLocal as db:
        stmt = delete(Sample).where(Sample.sample_id.in_(sample_ids))
        db.execute(stmt)
        db.commit()
        return None


def create_subject_conditions(subject_conditions: list[SubjectCondition]) -> None:
    with SessionLocal as db:
        db.add_all(subject_conditions)
        db.commit()
        return None


def get_subject_conditions_by_subject_id(
    subject_ids: Optional[list[str]],
) -> Sequence[Row[tuple[SubjectCondition]]]:
    with SessionLocal as db:
        stmt = select(SubjectCondition)
        if subject_ids:
            stmt = stmt.where(SubjectCondition.subject_id.in_(subject_ids))
        results = db.execute(stmt).all()
        return results


def update_subject_condition(subject_condition_record: SubjectCondition) -> None:
    with SessionLocal as db:
        stmt = (
            update(SubjectCondition)
            .where(
                SubjectCondition.subject_id == subject_condition_record.subject_id,
                SubjectCondition.condition_name
                == subject_condition_record.condition_name,
            )
            .values(**subject_condition_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_subject_conditions(subject_conditions: list[tuple[str, str]]) -> None:
    with SessionLocal as db:
        for subject_id, condition_name in subject_conditions:
            stmt = delete(SubjectCondition).where(
                SubjectCondition.subject_id == subject_id,
                SubjectCondition.condition_name == condition_name,
            )
            db.execute(stmt)
        db.commit()
        return None


def create_treatments(treatments: list[Treatment]) -> None:
    with SessionLocal as db:
        db.add_all(treatments)
        db.commit()
        return None


def get_treatments_by_subject_id(
    subject_ids: Optional[list[str]],
) -> Sequence[Row[tuple[Treatment]]]:
    with SessionLocal as db:
        stmt = select(Treatment)
        if subject_ids:
            stmt = stmt.where(Treatment.subject_id.in_(subject_ids))
        results = db.execute(stmt).all()
        return results


def update_treatment(treatment_record: Treatment) -> None:
    with SessionLocal as db:
        stmt = (
            update(Treatment)
            .where(
                Treatment.subject_id == treatment_record.subject_id,
                Treatment.subject_condition_name
                == treatment_record.subject_condition_name,
                Treatment.treatment_name == treatment_record.treatment_name,
            )
            .values(**treatment_record.__dict__)
        )
        db.execute(stmt)
        db.commit()
        return None


def delete_treatments(treatments: list[tuple[str, str, str]]) -> None:
    with SessionLocal as db:
        for subject_id, subject_condition_name, treatment_name in treatments:
            stmt = delete(Treatment).where(
                Treatment.subject_id == subject_id,
                Treatment.subject_condition_name == subject_condition_name,
                Treatment.treatment_name == treatment_name,
            )
            db.execute(stmt)
        db.commit()
        return None


def create_project_subject_connection(project_subject: ProjectSubject) -> None:
    with SessionLocal as db:
        db.add(project_subject)
        db.commit()
        return None


def get_project_subjects(
    project_ids: list[str],
) -> Sequence[Row[tuple[ProjectSubject]]]:
    with SessionLocal as db:
        stmt = select(ProjectSubject).where(ProjectSubject.project_id.in_(project_ids))
        results = db.execute(stmt).all()
        return results


def get_subject_projects(subject_ids: list[str]) -> Sequence[Row[tuple[Sample]]]:
    with SessionLocal as db:
        stmt = select(Sample).where(Sample.subject_id.in_(subject_ids))
        results = db.execute(stmt).all()
        return results


def delete_project_subject_connection(project_id: str, subject_id: str) -> None:
    with SessionLocal as db:
        stmt = delete(ProjectSubject).where(
            ProjectSubject.project_id == project_id,
            ProjectSubject.subject_id == subject_id,
        )
        db.execute(stmt)
        db.commit()
        return None
