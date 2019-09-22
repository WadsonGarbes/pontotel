from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from hashlib import md5

class Usuario(UserMixin, db.Model):
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

    def avatar(self, size):
        d = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(d,
                size)

    def __repr__(self):
        return '<Usuario: {}>'.format(self.nome)


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

