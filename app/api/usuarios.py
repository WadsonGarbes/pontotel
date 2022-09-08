from flask import jsonify, request, url_for, g, abort, Blueprint
from app import db
from app.models import Usuario
from app.api import api
from app.api.erros import bad_request
from app.api.auth import token_auth
import requests
from datetime import datetime
from apifairy import authenticate, body, response, other_responses, arguments

from app.api.schemas import PaginatedUserSchema, UserSchema, UnauthorizedSchema, InvalidPayloadSchema, PaginationSchema

usuarios = Blueprint('usuarios', __name__)


user_schema = UserSchema()

@usuarios.route('/usuarios/<int:id>', methods=['GET'])
@token_auth.login_required
@authenticate(token_auth)
def get_user(id):
    return jsonify(Usuario.query.get_or_404(id).to_dict())


@usuarios.route('/usuarios', methods=['GET'])
@token_auth.login_required
@authenticate(token_auth)
@arguments(PaginationSchema)
@response(PaginatedUserSchema)
def get_users(pagination_args):
    return Usuario.to_collection_dict(Usuario.query, pagination_args["page"], pagination_args["per_page"], 'usuarios.get_users') 


@usuarios.route('/usuarios', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
@other_responses({401: "Unauthorized. Check your payload", 400:  "Invalid request"})
def create_user(user):
    data = request.get_json() or user
    if 'login' not in data or 'email' not in data or 'senha' not in data:
        abort(401)
    if Usuario.query.filter_by(login=data['login']).first():
        abort(401)
    if Usuario.query.filter_by(email=data['email']).first():
        abort(401)
    user = Usuario()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


@usuarios.route('/usuarios/<int:id>', methods=['PUT'])
@token_auth.login_required
@authenticate(token_auth)
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = Usuario.query.get_or_404(id)
    data = request.get_json() or {}
    if 'login' in data and data['login'] != user.username and \
            Usuario.query.filter_by(username=data['login']).first():
        return bad_request('Use outro login!')
    if 'email' in data and data['email'] != user.email and \
            Usuario.query.filter_by(email=data['email']).first():
        return bad_request('Use outro email!')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())