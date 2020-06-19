from pathlib import Path
import os

path = Path(__file__).parent.absolute()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    path, "my-service-account.json"
)
