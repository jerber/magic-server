from pathlib import Path
import os
from dotenv import load_dotenv

SERVICE_ACCOUNT_NAME = "my-service-account.json"


def get_service_account_path():
    """Tries to get the google account credentials service account json in either
    the base directory or in the magic directory"""
    curr_dir_path = Path(__file__).parent.absolute()
    this_dir_service_path = curr_dir_path / SERVICE_ACCOUNT_NAME

    return (
        this_dir_service_path
        if this_dir_service_path.exists()
        else Path.cwd() / SERVICE_ACCOUNT_NAME
    )


env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# check either in the cwd or in this dir for the service account

service_account_path = get_service_account_path()
if service_account_path.exists():
    # will this work on windows?
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        *service_account_path.parts
    )

    os.environ["HasDB"] = "1"

    # create the firebase connection with the service account
    from magicdb import db

    db.conn
