from fastapi import APIRouter
from fastapi.responses import HTMLResponse


from api.services import (
    get_projects,
    data_overview,
    statistical_analysis,
    data_subset_analysis,
)  # type: ignore
# from schemas import PydProject, PydSubject, PydSample, PydTreatment


projects_router = APIRouter()
# subjects_router = APIRouter()
# samples_router = APIRouter()
# treatments_router = APIRouter()
user_stories_router = APIRouter()


@projects_router.get("/")
def read_projects(proj_id: str | None = None):
    projects = get_projects([proj_id] if proj_id else None)
    return projects


@user_stories_router.get("/data-overview", response_class=HTMLResponse)
def read_data_overview() -> str:
    return data_overview()


@user_stories_router.get("/statistical-analysis", response_class=HTMLResponse)
def read_statistical_analysis() -> str:
    return statistical_analysis()


@user_stories_router.get("/data-subset-analysis", response_class=HTMLResponse)
def read_data_subset_analysis() -> str:
    return data_subset_analysis()
