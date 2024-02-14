from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import psycopg2

# PostgreSQL database configuration
DATABASE_URL = "postgresql://root:root@localhost:5432/tasks_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

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
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tasks_db (name, image) VALUES (%s, %s) RETURNING id", (name, image))
        task_id = cur.fetchone()[0]
        conn.commit()
        return task_id
    finally:
        cur.close()
        conn.close()

@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    task_id = create_task_in_postgres(task.name, task.image)
    return {"id": task_id, "name": task.name, "image": task.image}

# Define a route for the root endpoint "/"
@app.get("/test")
def read_root():
    data = [{"id": 1, "name": "Jayantha BS", "Profession": "Fullstack Developer", "Experience": "5 Years",
            "company": ["EFI", "Risk Advisors Inc", "Medilenz", "CamcomAI","Open to work"],"hobi":"Cricket"
            }]
    return JSONResponse(content=data, headers={"Custom-Header": "value"})
