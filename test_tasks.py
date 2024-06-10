import pytest
#from fastapi.testclient import TestClient
#from sqlalchemy.orm import sessionmaker
#from main import SQLALCHEMY_DATABASE_URL

import random
import requests

# Если захотим добавить например модульные тесты, работающие с базой данных.
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
#Session = sessionmaker(bind=engine)
#session = Session()

#client = TestClient(app)


def test_get_tasks():
    url = "http://127.0.0.1:8000/tasks"
    headers = {"Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200

def test_get_task_1():
    url = "http://127.0.0.1:8000/tasks/1"
    headers = {"Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200
    print(resp.json())

# TODO: Use pytest's @mark.skip decorator.
def skip_test_create_task():
    url = "http://127.0.0.1:8000/tasks"    
    task_data = {
        #"id" : 4,
        "title": "New TaskTESTTESTT",
        "description": "KJFKSFLKHF",
        "status": "pending",
        #"created_at" : "2024-06-08T17:41:29",
        #"updated_at" : "2024-06-08T17:41:29",
    }

    headers = {"Content-Type": "application/json"}    
    response = requests.post(url, json=task_data, headers=headers)
    # Check if the request was successful
    if response.status_code == 201:
        print("Created task:", response.json()["id"])
    else:
        print("Error creating task:", response.text)
    assert response.status_code == 201, "WRONG STATUS CODE!!!"

def skip_test_update_task():
    url = "http://127.0.0.1:8000/tasks/1/"
    task_data = {"title":"NEW TITLE", "status":"pending"}
    headers = {"Content-Type": "application/json"}
    resp = requests.put(url, json=task_data, headers=headers)
    assert resp.status_code == 200


def test_create_get_update_delete_task():
    """
    Тестируем несколько эндпоинтов сразу.
    """
    ################# Create a task. #################
    url = "http://127.0.0.1:8000/tasks/"
    task_data = {
                "title": "Deleteme",
                "description": "This task should not persist in database.",
                "status": "pending",
                }
    headers = {"Content-Type": "application/json"}    
    response = requests.post(url, json=task_data, headers=headers)
    if response.status_code == 201:
        print("Task created successfully.")
        task_id = response.json()["id"]
        print("Created task id:" + str(task_id))
    else:
        print("Error creating task:", response.text)
    assert response.status_code == 201, "WRONG STATUS CODE!"

    ################# Update that task. #################
    url = f"http://127.0.0.1:8000/tasks/{task_id}/"
    task_data = {"title":"Updated title for test task.", 
                 "status":"completed", 
                 "description" : "Updated task description"}
    response = requests.put(url, json=task_data, headers=headers)
    if response.status_code == 200:
        task_id = response.json()["id"]
        print("Updated task id:" + str(task_id))
    else:
        print(response.status_code)
        print("Error updating task:", response.text)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title for test task."
    assert response.json()["description"] == "Updated task description"
    
    ################# Delete that task. #################
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Deleted tasl successfully.")
    else:
        print(response.status_code)
        print("Error deleting task:", response.status_code,response.text)
    assert response.status_code == 204
    
