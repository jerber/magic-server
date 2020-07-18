import requests

from main import use_host, port

# first start the sever w ./start
base_url = f"http://{use_host}:{port}"


def test_test_errors():
    valid_response = {"success": False, "message": "This test worked!"}
    response = requests.get(base_url + "/test_errors")
    print(response.json())
    assert response.status_code == 452
    assert response.json() == valid_response
