from app.magic.Services.Twilio import send_text
from fastapi import APIRouter

r = APIRouter()


@r.get("/send_text")
def send_text_router(phone_number: str, body: str):
    sid = send_text(to=phone_number, body=body)
    return sid


from app.magic import app

app.include_router(r, prefix="/text", tags=["text"])
