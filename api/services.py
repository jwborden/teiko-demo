from crud import get_project_by_project_id


def get_projects(project_ids: list[str] | None = None) -> list[str]:
    projects = get_project_by_project_id(project_ids if project_ids else None)
    out = [proj._mapping["Project"].project_id for proj in projects]
    return out
