from flask import Blueprint

api = Blueprint('api', __name__)

from . import cotacoes, erros,usuarios, tokens