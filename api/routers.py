from fastapi import APIRouter

from services import get_projects
from schemas import PydProject, PydSubject, PydSample, PydTreatment


projects_router = APIRouter()
subjects_router = APIRouter()
samples_router = APIRouter()
treatments_router = APIRouter()


@projects_router.get("/")
def read_projects(proj_id: str | None = None):
    projects = get_projects([proj_id] if proj_id else None)
    return projects
