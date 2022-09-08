import json
from lib2to3.pgen2 import token

from flask import g, Blueprint
from app import db
from app.api import api
from app.api.auth import basic_auth, token_auth
from apifairy import authenticate, body, response, other_responses
from app.api.schemas import TokenSchema

tokens = Blueprint('tokens', __name__)


token_schema = TokenSchema()

@tokens.route('/tokens', methods=["POST"])
@basic_auth.login_required
@authenticate(basic_auth)
@response(token_schema)
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return {"access_token": token}


@tokens.route('/tokens', methods=["DELETE"])
@token_auth.login_required
@authenticate(token_auth)
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
