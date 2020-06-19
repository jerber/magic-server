from pathlib import Path
import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)


path = Path(__file__).parent.absolute()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    path, "my-service-account.json"
)
