import random
import string


def random_str(n=50):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )
