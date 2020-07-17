from typing import List
from app.magic import router

from app.magic.Services.Email import send_email_in_background


@router.post("/send_email")
def send_email(body: str, recipients: List[str]):
    return send_email_in_background(text_body=body, recipients=recipients)
