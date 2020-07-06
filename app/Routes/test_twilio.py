from app.magic.Services.Twilio import send_text
from app.magic import router


@router.get("/send_text")
def send_text_router(phone_number: str, body: str):
    sid = send_text(to=phone_number, body=body)
    return sid
