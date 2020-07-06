from magicdb.Models import MagicModel


class CurrentUser(MagicModel):
    uid: str
    phone_number: str
    auth_time: int
    iat: int
    exp: int
    iss: str = None
    aud: str = None
    user_id: str = None
    sub: str = None
    firebase: dict = {}
