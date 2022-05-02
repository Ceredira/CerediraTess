__author__ = 'unixshaman'

from flask import Blueprint

from ceredira_tess.agents_locker import AgentsLocker

app = Blueprint('app', __name__, template_folder='templates')
agents_locker = AgentsLocker()


def generate_random_string(length):
    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    password = ''
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password
