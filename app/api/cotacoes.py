from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Cotacao
from app.api import api
from app.api.erros import bad_request
from app.api.auth import token_auth
import requests
from datetime import datetime


@api.route('/cotacoes/<int:id>', methods=['GET'])
@token_auth.login_required
def get_cotacao(id):
    return jsonify(Cotacao.query.get_or_404(id).to_dict())


@api.route('/cotacoes', methods=['GET'])
@token_auth.login_required
def get_cotacoes():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Cotacao.x(Cotacao.query, page, per_page,
            'api.get_cotacoes')
    return jsonify(data)


@api.route('/cotacoes', methods=['POST'])
@token_auth.login_required
def cadastrar_cotacao():
    data = request.get_json() or {}
    if 'data' not in data:
        return bad_request('Faltando o atributo data no JSON para chamar a API')
    cot = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BOVA11.SAO&apikey=0ED3YY5RQSO6UILH').json()
    cot = cot['Time Series (Daily)'][data['data']]
    cotacao = Cotacao(
        abertura=cot['1. open'],
        data_consulta=data['data'],
        data_cadastro=datetime.now(),
        maximo=cot['2. high'],
        minimo=cot['3. low'],
        fechamento=cot['4. close'],
        volume=cot['5. volume']
    )
    db.session.add(cotacao)
    db.session.commit()
    response = jsonify(cotacao.to_dict())
    response.status_code = 201
    response.headers['Localizacao'] = url_for('api.get_cotacao', id=cotacao.id)
    return response


@api.route('/cotacoes/<int:id>', methods=['PUT'])
@token_auth.login_required
def atualizar_cotacao(id):
    cotacao = Cotacao.query.get_or_404(id)
    data = request.get_json() or {}
    if 'data' not in data:
        cotacao.data_cadastro = str(datetime.now())
    if 'abertura' in data:
        cotacao.abertura = data['abertura']
    if 'fechamento' in data:
        cotacao.fechamento = data['fechamento']
    if 'maximo' in data:
        cotacao.maximo = data['maximo']
    if 'minimo' in data:
        cotacao.minimo = data['minimo']
    if 'volume' in data:
        cotacao.volume = data['volume']
    db.session.commit()
    return jsonify(cotacao.to_dict())


@api.route('/cotacoes/<int:id>', methods=['DELETE'])
@token_auth.login_required
def deletar_cotacao(id):
    cot = Cotacao.query.get_or_404(id)
    response = jsonify(cot.to_dict())
    db.session.delete(cot)
    db.session.commit()
    response.status_code = 204
    return response

