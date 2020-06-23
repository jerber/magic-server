from pathlib import Path
import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


curr_dir_path = Path(__file__).parent.absolute()
service_account_name = "my-service-account.json"

service_account_path = Path(curr_dir_path) / service_account_name

if service_account_path.exists():
    # will this work on windows?
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        *service_account_path.parts
    )

    os.environ["HasDB"] = "1"

    # create the firebase connection with the service account
    from magicdb import db

    db.conn
