from pathlib import Path
import os
from pydantic import BaseSettings


def config_firestore(service_account_name):
    service_account_path = find_file(service_account_name)
    if service_account_path.exists():
        # will this work on windows?
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
            *service_account_path.parts
        )

        os.environ["HasDB"] = "1"

        # create the firebase connection with the service account
        from magicdb import db

        db.conn


def find_file(glob_string: str, levels: int = 7):
    d = Path.cwd()
    for _ in range(levels):
        envs = list(d.glob(glob_string))
        if envs:
            return envs[0]
        d = d.parent


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

    # for email
    email_port: int = 465
    email_smtp_server: str = "smtp.gmail.com"
    sender_email: str
    sender_password: str

    # for mailgun
    mailgun_private_api_key: str = None
    mailgun_domain_name: str = None
    mailgun_sender_name: str = None
    mailgun_sender_email: str = None

    # for magic link
    company_name: str = None

    # for stripe
    stripe_api_key: str = None

    class Config:
        env_file = find_file(glob_string="*.env") or ".env"


# If you want to make the env variables from .env available
# from dotenv import load_dotenv
# if os.path.exists(env_path):
#     load_dotenv(env_path)

settings = Settings()

config_firestore(settings.service_account_name)
