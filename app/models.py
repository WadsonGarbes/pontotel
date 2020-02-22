import os
import base64
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from hashlib import md5


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Usuario(UserMixin, PaginatedAPIMixin, db.Model):
    """
    Cria uma tabela Usuarios
    """

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    login = db.Column(db.String(60), index=True, unique=True)
    nome = db.Column(db.String(60), index=True)
    sobrenome = db.Column(db.String(60), index=True)
    senha_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    @property
    def password(self):
        """
        Previne o acesso à senha
        """
        raise AttributeError('A senha não é um atributo legível.')

    @password.setter
    def password(self, senha):
        """
        Hasheia a senha
        """
        self.senha_hash = generate_password_hash(senha)

    def verify_password(self, senha):
        """
        Verifica o hash da senha
        """
        return check_password_hash(self.senha_hash, senha)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def avatar(self, size):
        d = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(d,
                size)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Usuario.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return '<Usuario: {}>'.format(self.nome)

    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'login': self.login,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['login', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'senha' in data:
            self.set_password(data['senha'])


@login.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Empresa(db.Model):
    """
    Cria a tabela empresa
    """

    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    simbolo = db.Column(db.String(50), unique=True)
    tipo = db.Column(db.String(50)) 
    regiao = db.Column(db.String(50)) 
    abertura = db.Column(db.String(50)) 
    fechamento = db.Column(db.String(50)) 
    zona = db.Column(db.String(50)) 
    moeda = db.Column(db.String(50))
    cotacoes = db.relationship('Cotacao', backref='empresa', lazy='dynamic')

    def __repr__(self):
        return '<Empresa: {}>'.format(self.nome)


class Cotacao(db.Model):
    """
    Cria a tabela cotacao
    """

    __tablename__ = 'cotacoes'

    id = db.Column(db.Integer, primary_key=True)
    data_consulta = db.Column(db.String(60))
    data_cadastro = db.Column(db.String(60))
    abertura = db.Column(db.Float)
    maximo = db.Column(db.Float) 
    minimo = db.Column(db.Float) 
    fechamento = db.Column(db.Float) 
    volume = db.Column(db.Integer) 
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))


    def __repr__(self):
        return '<Cotacao: {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'data_consulta': self.data_consulta,
            'data_cadastro': self.data_cadastro,
            'abertura': self.abertura,
            'maximo': self.maximo,
            'minimo': self.minimo,
            'fechamento': self.fechamento,
            'volume': self.volume
        }
        return data

    def x(query, page, per_page, endpoint, **kwargs):
        recursos = query.paginate(page, per_page, False)
        data = {
            'itens': [item.to_dict() for item in recursos.items],
            '_meta': {
                'pagina': page,
                'por_pagina:': per_page,
                'total_de_pagina': recursos.pages,
                'total_de_itens': recursos.total
            },
            '_links': {
                'proprio': url_for(endpoint, page=page, per_page=per_page,
                                   **kwargs),
                'proximo': url_for(endpoint, page=page + 1, per_page=per_page,
                                   **kwargs) if recursos.has_next else None,
                'anterior': url_for(endpoint, page=page - 1, per_page=per_page,
                                   **kwargs) if recursos.has_prev else None, 
            }
        }
        return data

    def from_dict(self, data):
        for field in ['data', 'abertura', 'fechamento', 'maximo', 'minimo', 'volume']:
            if field in data:
                setattr(self, field, data[field])
