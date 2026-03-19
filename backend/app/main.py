from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.core.config import settings
from app.db.database import init_db
from app.api import auth, tasks

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API with JWT authentication",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Serve frontend static files if present
frontend_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Task Manager API is running"}


@app.on_event("startup")
def on_startup():
    init_db()
