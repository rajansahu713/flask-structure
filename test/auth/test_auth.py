import requests
import json
import jsonpath
import pytest


urls = "http://127.0.0.1:5000/api/v1/auth"

def test_login():
    body={
            "email": "admin123@gmail.com",
            "password": "123456789"
        }
    
    path=f"{urls}/login"
    data=json.dumps(body)
    response = requests.post(path,data=data,headers={"Content-Type":"application/json"})
    assert response.status_code==200

def test_register():
    body={"username":"admin1234","email":"admin1234@gmail.com","password":"123456789"}

    path =f"{urls}/register"
    data=json.dumps(body)
    response = requests.post(path,data=data, headers={"Content-Type":"application/json"})

    assert response.status_code==201

def test_generate_refresh():
    path =f"{urls}/token/refresh"
    response = requests.post(path,headers={"Content-Type":"application/json", "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTA0MjYyNiwianRpIjoiNzM1YzY5YWYtNzgzMC00YzE3LWJjOWMtZDQzNjhmYWRlMzY5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY1MTA0MjYyNiwiZXhwIjoxNjUzNjM0NjI2fQ.rMImkd7zA2lc86vlYcT_ULbCosCOh2M1ol9OGbYUvog"})
    
    assert response.status_code==200
