import time
import os

import requests

from main import use_host, port

# first start the sever w ./start
base_url = f"http://{use_host}:{port}"
# are you using real url and real db?
if os.getenv("aws") or True:
    real_url = f"https://jeremyberman.org/dev"
    base_url = real_url


def test_root():
    response = requests.get(base_url + "/")
    assert response.status_code == 200


def test_test_errors():
    valid_response = {"success": False, "message": "This test worked!"}
    response = requests.get(base_url + "/test_errors")
    print(response.json())
    assert response.status_code == 452
    assert response.json() == valid_response


def test_background_tasks_via_call():
    from app.magic.Models.Call import Call
    from app.magic.Utils.random_utils import random_str

    code = random_str(30)
    url = f"{base_url}/test_errors?{code}=yes"
    response = requests.get(url=url)
    assert response.status_code == 452
    time.sleep(5)  # give time to write to DB
    calls = Call.collection.where("request.url", "==", url).stream()
    assert len(calls) == 1
