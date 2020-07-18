import stripe
from app.magic.config import settings

stripe.api_key = settings.stripe_api_key
