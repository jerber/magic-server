from twilio.rest import Client
import os
from functools import wraps
from app.magic.config import settings

from app.magic.Errors import TwilioException


try:
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
except Exception as e:
    print("Twilio SID or AUTH TOKEN not given.")

FROM_NUMBER = os.environ.get("FROM_NUMBER")


def need_twilio_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [settings.twilio_account_sid, settings.twilio_auth_token]
        if None in twilio_vars:
            raise TwilioException(
                message="Not all Twilio credentials found in .env file. Need TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
            )
        return f(*args, **kwargs)

    return wrapper


def need_copilot_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [settings.twilio_messaging_service_sid]
        if None in twilio_vars:
            raise TwilioException(
                message="Not all Twilio co-pilot credentials found in .env file. Need MESSAGING_SERVICE_SID."
            )
        return f(*args, **kwargs)

    return wrapper


@need_twilio_vars
def send_text(to, body, from_number=FROM_NUMBER):
    message = client.messages.create(body=body, from_=from_number, to=to,)
    return message.sid


@need_twilio_vars
def send_text_with_copilot(to, body, status_callback=settings.twilio_status_callback):
    message = client.messages.create(
        body=body,
        messaging_service_sid=settings.twilio_messaging_service_sid,
        to=to,
        status_callback=status_callback,
    )
    return message.sid
