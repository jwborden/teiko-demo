from pydantic import BaseModel


class PydImport(BaseModel):
    project: str
    subject: str
    condition: str | None = None
    age: int | None = None
    sex: str | None = None
    treatment: str | None = None
    response: str | None = None
    sample: str | None = None
    sample_type: str | None = None
    time_from_treatment_start: int | None = None
    b_cell: int | None = None
    cd8_t_cell: int | None = None
    cd4_t_cell: int | None = None
    nk_cell: int | None = None
    monocyte: int | None = None


class PydProject(BaseModel):
    project_id: str


class PydSubject(BaseModel):
    subject_id: str
    age: int | None = None
    sex: str | None = None


class PydSample(BaseModel):
    sample_id: str
    sample_type: str | None = None
    time_from_treatment_start: int | None = None
    b_cell: int | None = None
    cd8_t_cell: int | None = None
    cd4_t_cell: int | None = None
    nk_cell: int | None = None
    monocyte: int | None = None
    subject_id: str


class PydSubjectCondition(BaseModel):
    subject_id: str
    condition_name: str


class PydTreatment(BaseModel):
    subject_id: str
    subject_condition_name: str
    treatment_name: str
    response: bool | None = None


class PydProjectSubjects(BaseModel):
    project_id: str
    subject_id: str
