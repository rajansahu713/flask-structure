import requests
import json
import jsonpath
import pytest


urls = "http://127.0.0.1:5000/api/v1/auth"

def test_bookmarks():
    # body="""{
    #     "name": "morpheus",
    #     "job": "leader"
    # }"""
    # request_json = json.loads(body)
    response = requests.post(urls,request_json)
    assert response.status_code==201