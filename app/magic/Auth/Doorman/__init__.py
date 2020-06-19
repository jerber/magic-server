import requests
import os

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .CurrentUser import CurrentUser

from app.magic import router
from firebase_admin import auth


LOCATION, PROJECT_ID = (
    os.environ.get("CLOUD_FUNCTION_LOCATION"),
    os.environ.get("FIREBASE_PROJECT_ID"),
)

print("LOCATION", LOCATION, "PROJECT_ID", PROJECT_ID)
ID_TOKEN_ENDPOINT: str = f"https://{LOCATION}-{PROJECT_ID}.cloudfunctions.net/getIdToken"
DOORMAN_BACKEND_ENDPOINT: str = "https://sending-messages-for-doorman.herokuapp.com/phoneLogic"

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/login_with_phone")
def login_with_phone(phone_number: str):
    body = {
        "action": "loginWithPhone",
        "phoneNumber": phone_number,
        "publicProjectId": os.environ.get("DOORMAN_PUBLIC_PROJECT_ID"),
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    return resp


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("form_data", form_data.username, form_data.password)

    body = {
        "action": "verifyCode",
        "phoneNumber": form_data.username,
        "code": form_data.password,
        "publicProjectId": os.environ.get("DOORMAN_PUBLIC_PROJECT_ID"),
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    backend_token = resp.get("token")
    if not backend_token:
        print(resp)
        return resp

    id_resp = requests.post(ID_TOKEN_ENDPOINT, json={"token": backend_token}).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        return id_resp

    return {"access_token": id_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oath2_scheme)):
    print("TOKKKKK", token)
    decoded = auth.verify_id_token(token)
    print("doceded", decoded)
    current_user = CurrentUser(**decoded)
    print("current user", current_user)
    return current_user


@router.get("/secure_things")
def get_secure_things(
    message: str, current_user: CurrentUser = Depends(get_current_user)
):
    print("message", message)
    print("this is the current authed user!", current_user)
    return current_user
