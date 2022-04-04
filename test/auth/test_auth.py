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
    #request_json = json.loads(body)
    path=f"{urls}/login"
    response = requests.post(path,data=json.dump(body))
    print(response.text)
    print(response.status_code)
    assert response.status_code==200

def test_register():
    body={"username":"admin1234","email":"admin1234@gmail.com","password":"123456789"}

    path =f"{urls}/register"
    #request_json = json.loads(body)
    response = requests.post(path,data=json.dumps(body))
    print(response.text)

    assert response.status_code==201