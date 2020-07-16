from pathlib import Path
import os
from pydantic import BaseSettings


def get_service_account_path(service_account_name):
    """Tries to get the google account credentials service account json in either
    the base directory or in the magic directory"""
    curr_dir_path = Path(__file__).parent.absolute()
    this_dir_service_path = curr_dir_path / service_account_name

    return (
        this_dir_service_path
        if this_dir_service_path.exists()
        else Path.cwd() / service_account_name
    )


def config_firestore(service_account_name):
    service_account_path = get_service_account_path(service_account_name)
    if service_account_path.exists():
        # will this work on windows?
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
            *service_account_path.parts
        )

        os.environ["HasDB"] = "1"

        # create the firebase connection with the service account
        from magicdb import db

        db.conn


env_path = os.path.join(os.getcwd(), ".env")
if not os.path.exists(env_path):
    env_path = ".env"


class Settings(BaseSettings):
    app_name: str = "GOAT Server"
    version: str = "0.0.1"

    # for dev
    print_level = 1

    # will be loaded first
    local: bool = False

    # for firestore
    service_account_name = "my-service-account.json"

    # for doorman
    doorman_public_project_id: str = None
    firebase_project_id: str = None
    cloud_function_location: str = None

    # for twilio
    twilio_account_sid: str = None
    twilio_auth_token: str = None
    twilio_messaging_service_sid: str = None
    twilio_status_callback: str = None
    from_number: str = None

    # for segment
    segment_write_key: str = None

    # for dynamo
    tasks_table_name: str = None

    # for routing
    stage: str = "dev"

    # for saving calls
    save_calls: bool = True

    class Config:
        env_file = env_path


# If you want to make the env variables from .env available
# from dotenv import load_dotenv
# if os.path.exists(env_path):
#     load_dotenv(env_path)

settings = Settings()

config_firestore(settings.service_account_name)
