from twilio.rest import Client
import os
from functools import wraps


from app.magic.Errors import TwilioException

STATUS_CALLBACK = os.environ.get("TWILIO_STATUS_CALLBACK")
MESSAGING_SERVICE_SID = os.environ.get("TWILIO_MESSAGING_SERVICE_SID")

SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

try:
    client = Client(SID, AUTH_TOKEN)
except Exception as e:
    print("Twilio SID or AUTH TOKEN not given.")

FROM_NUMBER = os.environ.get("FROM_NUMBER")


def need_twilio_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [SID, AUTH_TOKEN]
        if None in twilio_vars:
            raise TwilioException(
                message="Not all Twilio credentials found in .env file. Need TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
            )
        return f(*args, **kwargs)

    return wrapper


def need_copilot_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [MESSAGING_SERVICE_SID]
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
def send_text_with_copilot(to, body, status_callback=STATUS_CALLBACK):
    message = client.messages.create(
        body=body,
        messaging_service_sid=MESSAGING_SERVICE_SID,
        to=to,
        status_callback=status_callback,
    )
    return message.sid
