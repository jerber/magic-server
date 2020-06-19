import requests
import os

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .CurrentUser import CurrentUser

from app.magic import router

# constants
# DOORMAN_PUBLIC_PROJECT_ID: str = "5BkiNVFpQOUidurgrYrW"  # for serverX
# FIREBASE_PROJECT_ID: str = "serverx-fa37c"  # for serverX
# CLOUD_FUNCTION_LOCATION: str = "us-central1"

LOCATION, PROJECT_ID = (
    os.environ.get("CLOUD_FUNCTION_LOCATION"),
    os.environ.get("FIREBASE_PROJECT_ID"),
)
ID_TOKEN_ENDPOINT: str = f"https://{LOCATION}-{PROJECT_ID}.cloudfunctions.net/getIdToken"
DOORMAN_BACKEND_ENDPOINT: str = "https://sending-messages-for-doorman.herokuapp.com/phoneLogic"

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/login_with_phone", response_model=dict)
def login_with_phone(phone_number: str):
    body = {
        "action": "loginWithPhone",
        "phoneNumber": phone_number,
        "publicProjectId": DOORMAN_PUBLIC_PROJECT_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    return resp
