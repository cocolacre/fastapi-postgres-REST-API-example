from fastapi import FastAPI, HTTPException
from fastapi import status, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
import logging

# db setup
SQLALCHEMY_DATABASE_URL = "postgresql://cocolacre:123456@localhost/myappdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

#fastapi app init
app = FastAPI()

# logging basic setup
logging.basicConfig(level=logging.DEBUG, filename='tasks_app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Loading app.")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, server_default="now()")
    #created_at = Column(DateTime(precision=0), server_default="now()") 
    updated_at = Column(DateTime, server_default="now()", onupdate="now()")


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              schema_extra={
                                "example": {
                                "id": 1,
                                "title": "My Task",
                                "description": "This is my task",
                                "status": "pending",
                                "updated_at": "2024-06-09T12:00:00"
                                }
                            })
    #https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.from_attributes
    id: int | None = None
    title: str
    description: str | None = None #optional
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@app.get("/tasks/")
async def get_tasks():
    logger.debug("/tasks/ accessed with a GET request.")
    tasks = session.query(Task).all()
    return {"tasks": [TaskSchema.from_orm(task) for task in tasks]}


@app.get("/tasks/{task_id}/")
async def get_task(task_id: int):
    logger.debug(f"/tasks/{task_id} accessed with a GET request.")
    task = session.query(Task).get(task_id)
    #task = session.query(Task).filter(Task.id == task_id).first()
    if task is None:
        logger.debug(f"Client requested task_id={task_id}, but it is not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSchema.from_orm(task)


@app.post("/tasks/")
async def create_task(task: TaskSchema):
    logger.debug(f"/tasks/ accessed with a POST request.")
    new_task = Task(**task.dict())
    session.add(new_task)
    try:
        session.commit()
    except IntegrityError:
        logger.debug(f"Client requested task_id={task_id}, but it is not found.")
        raise HTTPException(status_code=400, detail="IntegrityError occured upon creating a task.")
    return JSONResponse(status_code=201, content={"id": new_task.id})


@app.put("/tasks/{task_id}/")
async def update_task(task_id: int, task: TaskSchema):
    logger.debug(f"/tasks/{task_id} accessed with a PUT request.")
    task_db = session.query(Task).get(task_id)
    if task_db is None:
        logger.debug(f"Client requested to update task_id={task_id}, but it is not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    task_db.title = task.title
    task_db.description = task.description
    task_db.status = task.status
    session.commit()
    return TaskSchema.from_orm(task_db)


#async def delete_task(task_id: int, status_code=status.HTTP_204_NO_CONTENT, response_class=Response):
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    logger.debug(f"/tasks/{task_id} accessed with a DELETE request.")
    task = session.query(Task).get(task_id)
    if task is None:
        logger.debug(f"Client requested to delete {task_id=}, but it is not found.")
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    #return JSONResponse(status_code=204, content={"task_id":task_id})
    #return None
    return Response(status_code=status.HTTP_204_NO_CONTENT)




































blackbox_ai_hints = """

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from enum import Enum

# Define the Postgres connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
SQLALCHEMY_DATABASE_URL = "postgresql://cocolacre:123456@localhost/myappdb"
SQLALCHEMY_DATABASE_URL = "postgresql://cocolacre:123456@localhost/myappdb"
# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker
Session = sessionmaker(bind=engine)

# Create a base class for our models
Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)  # We'll use an Enum for this field
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(DateTime, server_default="now()", onupdate="now()")

# Define the TaskStatus Enum
class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

# Define the TaskSchema
class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime

# Create the app
app = FastAPI()

# Create a session
session = Session()

# Define the API endpoints
@app.get("/tasks/")
async def read_tasks():
    tasks = session.query(Task).all()
    return {"tasks": [TaskSchema.from_orm(task) for task in tasks]}

@app.get("/tasks/{task_id}/")
async def read_task(task_id: int):
    task = session.query(Task).get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSchema.from_orm(task)

@app.post("/tasks/")
async def create_task(task: TaskSchema):
    new_task = Task(**task.dict())
    session.add(new_task)
    try:
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Task with same title already exists")
    return JSONResponse(status_code=201, content={"task_id": new_task.id})

@app.put("/tasks/{task_id}/")
async def update_task(task_id: int, task: TaskSchema):
    task_db = session.query(Task).get(task_id)
    if task_db is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db.title = task.title
    task_db.description = task.description
    task_db.status = task.status
    session.commit()
    return TaskSchema.from_orm(task_db)

@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    task = session.query(Task).get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return JSONResponse(status_code=204)
    
    
"""