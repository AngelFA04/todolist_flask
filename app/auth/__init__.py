from flask import Blueprint

# Blueprint app with name auth, referenced the name
# of this file, the prefix means that all the routes
# that begin with /auth are going to be redirected here
auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import views
