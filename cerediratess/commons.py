__author__ = 'unixshaman'

from flask import Blueprint

from cerediratess.agents_locker import AgentsLocker

app = Blueprint('app', __name__, template_folder='templates')
agents_locker = AgentsLocker()
