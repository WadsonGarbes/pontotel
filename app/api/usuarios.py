from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Usuario
from app.api import api
from app.api.erros import bad_request
from app.api.auth import token_auth
import requests
from datetime import datetime


@api.route('/usuarios/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(Usuario.query.get_or_404(id).to_dict())


@api.route('/usuarios', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Usuario.to_collection_dict(Usuario.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api.route('/usuarios', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'login' not in data or 'email' not in data or 'senha' not in data:
        return bad_request('deve incluir login, email e senha!')
    if User.query.filter_by(username=data['login']).first():
        return bad_request('Por favor use outro login')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('Por favor use outro endereço de email')
    user = Usuario()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api.route('/usuarios/<int:id>', methods=['PUT'])
@token_auth.login_required
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