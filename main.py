from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://root:root@postgres:5432/tasks_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String)

Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    name: str
    image: str

class TaskResponse(BaseModel):
    id: int
    name: str
    image: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://example.com", "http://localhost:30"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_task_in_db(db: Session, name: str, image: str) -> int:
    task = Task(name=name, image=image)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task.id

def get_task_from_db(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_in_db(db: Session, task_id: int, name: str, image: str) -> Task:
    task = get_task_from_db(db, task_id)
    if task:
        task.name = name
        task.image = image
        db.commit()
        db.refresh(task)
    return task

def delete_task_from_db(db: Session, task_id: int) -> Task:
    task = get_task_from_db(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task

# Define Redis caching decorator
def cache(seconds):
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            key = f.__name__ + ":" + "_".join(map(str, args)) + "_" + "_".join(map(str, kwargs.items()))
            # Check if data is present in cache
            cached_data = redis_client.get(key)
            if cached_data:
                return JSONResponse(content=cached_data, headers={"Cache-Control": f"max-age={seconds}"})
            else:
                # Execute the original function
                result = f(*args, **kwargs)
                # Store result in cache
                redis_client.setex(key, seconds, result)
                return result
        return wrapper
    return decorator


# CRUD operations with caching
@app.post("/tasks/", response_model=TaskResponse)
@cache(seconds=60)  # Cache for 60 seconds
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task_id = create_task_in_db(db, task.name, task.image)
    return {"id": task_id, "name": task.name, "image": task.image}

@app.get("/tasks/{task_id}", response_model=TaskResponse)
@cache(seconds=60)  # Cache for 60 seconds
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_from_db(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task.id, "name": task.name, "image": task.image}

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = update_task_in_db(db, task_id, task.name, task.image)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Invalidate cache for this task
    invalidate_cache("read_task", task_id)
    return {"id": updated_task.id, "name": updated_task.name, "image": updated_task.image}

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task_from_db(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Invalidate cache for this task
    invalidate_cache("read_task", task_id)
    return {"id": deleted_task.id, "name": deleted_task.name, "image": deleted_task.image}

# Function to invalidate cache for a specific CRUD operation and task ID
def invalidate_cache(operation: str, task_id: int):
    key = operation + ":" + str(task_id)
    redis_client.delete(key)
