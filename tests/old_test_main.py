import os


def make_test_env():
    os.environ["LOCAL"] = "1"
    os.environ["SERVICE_ACCOUNT_NAME"] = "my-service-account.json"


from fastapi.testclient import TestClient


from app.magic import app, settings, router, background_router

# from main import app

app.include_router(router)
app.include_router(background_router)
client = TestClient(app)


def test_test_errors():
    valid_response = {"success": False, "message": "This test worked!"}
    response = client.get("/test_errors")
    print(response.json())
    assert response.status_code == 452
    assert response.json() == valid_response


"""Do doorman tests maybe?"""


# test_test_errors()
