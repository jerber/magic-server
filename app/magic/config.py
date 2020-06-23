from pathlib import Path
import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


path = Path(__file__).parent.absolute()

service_account_name = "my-service-account.json"

if Path(service_account_name).exists():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        path, service_account_name
    )

    # create the firebase connection with the service account
    from magicdb import db

    db.conn
