from urllib import response
import requests
import json


urls="http://127.0.0.1:5000/api/v1/bookmarks"
token ="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTA0ODUwOSwianRpIjoiYzQzYmM4NjgtNWE0OS00ZTBhLTkwZDYtMzBkY2FiOGIyZWNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjUxMDQ4NTA5LCJleHAiOjE2NTEwNDk0MDl9.M6gaEsu3FFaQAauclsC-VgHcUitURiCsISLHmXWDogk"

def test_bookmarks_post():
    body= {
        "body": "Python.instruction",
        "url": "https://www.instagram.com/python.instructions/1246"
    }
    path = f'{urls}/'
    data = json.dumps(body)
    response = requests.post(path,data=data, headers={"Content-Type":"application/json","Authorization":token})

    assert response.status_code==201

def test_bookmarks_get_all():
    path = f'{urls}/'
    response = requests.get(urls, headers={"Content-Type":"application/json", "Authorization":token})

    assert response.status_code==200


def test_bookmarks_get_particular_records():
    path = f'{urls}/1'
    response = requests.get(urls, headers={"Content-Type":"application/json", "Authorization":token})

    
    assert response.status_code==200

def test_bookmarks_delete():
    path =f"{urls}/11"

    response = requests.delete(path, headers={"Content-Type":"application/json", "Authorization":token})

    assert response.status_code==200


def test_bookmarks_get_stats():
    path = f'{urls}/stats'
    response = requests.get(path, headers={"Content-Type":"application/json", "Authorization":token})

    assert response.status_code==200

def test_bookmarks_patch():
    path=f"{urls}/10"
    body= {
        "url": "https://www.instagram.com/hdshfh"
    }

    data = json.dumps(body)

    response = requests.patch( path, data=data, headers={"Content-Type":"application/json", "Authorization":token})
    
    assert response.status_code==200


