import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers import (
    projects_router,
    subjects_router,
    samples_router,
    treatments_router,
)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/html", response_class=HTMLResponse)
def read_html():
    from api.services import basic_html

    return basic_html()


app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(subjects_router, prefix="/subjects", tags=["subjects"])
app.include_router(samples_router, prefix="/samples", tags=["samples"])
app.include_router(treatments_router, prefix="/treatments", tags=["treatments"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
