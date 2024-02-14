from fastapi import FastAPI, HTTPException
from redis import Redis
import asyncpg
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://root:root@postgres:5432/tasks_db"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()

# Define SQLAlchemy model
class Task(Base):
    __tablename__ = "tasks_db"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String)

# Define Pydantic models for request and response schemas
class TaskCreate(BaseModel):
    name: str
    image: str

class TaskResponse(BaseModel):
    id: int
    name: str
    image: str


app = FastAPI()

# CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://example.com", "http://localhost:30"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_task_in_postgres(name: str, image: str):
    db = SessionLocal()
    try:
        task = Task(name=name, image=image)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id
    finally:
        db.close()

# Define a route for the root endpoint "/"
@app.get("/test")
def read_root():
    data = [{"id": 1, "name": "Jayantha BS", "Profession": "Fullstack Developer", "Experience": "5 Years",
            "company": ["EFI", "Risk Advisors Inc", "Medilenz", "CamcomAI","Open to work"],"hobi":"Cricket"
            }]
    return JSONResponse(content=data, headers={"Custom-Header": "value"})


@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    task_id = create_task_in_postgres(task.name, task.image)
    return {"id": task_id, "name": task.name, "image": task.image}
