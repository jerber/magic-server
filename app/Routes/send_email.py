from typing import List

from app.magic import router

# from app.magic.Services.Email import send_email_in_background
from app.magic.Services.Mailgun import send_email as send_email_mailgun


@router.post("/send_email")
def send_email(*, subject: str = None, email_body: str, recipients: List[str]):
    # return send_email_in_background(text_body=body, recipients=recipients)
    res = send_email_mailgun(text=email_body, recipients=recipients, subject=subject)
    return res.content
