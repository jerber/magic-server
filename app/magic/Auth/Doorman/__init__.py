import requests
import os
from functools import wraps

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .CurrentUser import CurrentUser

from app.magic import router
from firebase_admin import auth

from .errors import DoormanAuthException


LOCATION, PROJECT_ID, DOORMAN_ID = (
    os.environ.get("CLOUD_FUNCTION_LOCATION", "us-central1"),
    os.environ.get("FIREBASE_PROJECT_ID"),
    os.environ.get("DOORMAN_PUBLIC_PROJECT_ID"),
)

ID_TOKEN_ENDPOINT: str = f"https://{LOCATION}-{PROJECT_ID}.cloudfunctions.net/getIdToken"
DOORMAN_BACKEND_ENDPOINT: str = "https://sending-messages-for-doorman.herokuapp.com/phoneLogic"

token_url = "/token" if os.environ.get("LOCAL") else "/dev/token"
oath2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


def need_doorman_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        doorman_vars = [LOCATION, PROJECT_ID, DOORMAN_ID]
        if None in doorman_vars:
            raise DoormanAuthException(
                message="Not all Doorman credentials found in .env file. Need DOORMAN_PUBLIC_PROJECT_ID, "
                "FIREBASE_PROJECT_ID, and CLOUD_FUNCTION_LOCATION"
            )
        return f(*args, **kwargs)

    return wrapper


@router.post("/login_with_phone")
@need_doorman_vars
def login_with_phone(phone_number: str):
    body = {
        "action": "loginWithPhone",
        "phoneNumber": phone_number,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    return resp


@router.post("/token")
@need_doorman_vars
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    body = {
        "action": "verifyCode",
        "phoneNumber": form_data.username,
        "code": form_data.password,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    backend_token = resp.get("token")
    if not backend_token:
        print(resp)
        raise DoormanAuthException(message=str(resp))

    id_resp = requests.post(ID_TOKEN_ENDPOINT, json={"token": backend_token}).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        raise DoormanAuthException(message=str(id_resp))

    return {"access_token": id_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oath2_scheme)):
    decoded = auth.verify_id_token(token)
    current_user = CurrentUser(**decoded)
    return current_user


@router.get("/get_current_user", response_model=CurrentUser)
def get_current_user(current_user: CurrentUser = Depends(get_current_user)):
    return current_user
