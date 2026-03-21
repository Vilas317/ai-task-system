from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tasks, documents, search, analytics
from app.core.database import engine, Base

# Import all models so SQLAlchemy knows about them before creating tables
from app.models import user, task, document, activity_log, search_log

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Task & Knowledge Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/auth",      tags=["Authentication"])
app.include_router(tasks.router,     prefix="/tasks",     tags=["Tasks"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(search.router,    prefix="/search",    tags=["Search"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "AI Task & Knowledge Management System is running!"}