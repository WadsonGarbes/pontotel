from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Cotacao
from app.api import api
from app.api.erros import bad_request

@api.route('/cotacoes/<int:id>', methods=['GET'])
def get_cotacao(id):
    return jsonify(Cotacao.query.get_or_404(id).to_dict())