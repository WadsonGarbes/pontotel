#!/usr/bin/env python
# tests.py

import requests
import unittest
import os

from datetime import datetime
from flask_testing import TestCase
from app import create_app, db
from app.models import Usuario, Cotacao, Empresa
from config import Config

from flask import abort, url_for

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestBase(TestCase):

    def create_app(self):

        # Configurações dos testes
        app = create_app(TestConfig)
        return app

    def setUp(self):
        """
        Será chamado antes de cada teste
        """

        db.create_all()

        # cria usuario teste
        user = Usuario(nome="Pontotel", password="123", email='pontotel@pontotel.com')

        # salva usuário no banco de dados
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Será chamado após cada teste
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_usuario_model(self):
        """
        Testa número de registros na tabela Usuario
        """
        self.assertEqual(Usuario.query.count(), 1)

    def test_empresa_model(self):
        """
        Testa número de empresas do banco
        """

        # cria empresa de teste com base em chamada de api
        # muitas chamadas podem causar instabilidade no serviço
        # descomente apenas se achar necessário
        
        """
        emp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BOVA11&apikey=0ED3YY5RQSO6UILH').json()
        emp = emp['bestMatches'][0]
        empresa = Empresa(
            nome=emp['2. name'],
            simbolo=emp['1. symbol'],
            tipo=emp['3. type'],
            regiao=emp['4. region'],
            abertura=emp['5. marketOpen'],
            fechamento=emp['6. marketClose'],
            zona=emp['7. timezone'],
            moeda=emp['8. currency']
        )        
        """
        # comente esta seção caso utilize a seção acima
        empresa = Empresa(
            nome='Teste',
            simbolo='Teste',
            tipo='Teste',
            regiao='Teste',
            abertura='Teste',
            fechamento='Teste',
            zona='Teste',
            moeda='Teste'
            )
        # salva empresa no banco
        db.session.add(empresa)
        db.session.commit()

        self.assertEqual(Empresa.query.count(), 1)

    def test_cotacao_model(self):
        """
        Testa número cotações do banco
        """

        # cria cotacao teste com base em api

        # muitas chamadas podem causar instabilidade no serviço
        # descomente apenas se achar necessário
        '''
        cot = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BOVA11.SAO&apikey=0ED3YY5RQSO6UILH').json()
        cot = cot['Time Series (Daily)']['2019-09-09']
        cotacoes = Cotacao(
            abertura=cot['1. open'],
            data=datetime.now,
            maximo=cot['2. high'],
            minimo=cot['3. low'],
            fechamento=cot['4. close'],
            volume=cot['5. volume']
        )
        db.session.add(cotacoes)
        db.session.commit()
        '''
        cotacoes = Cotacao(
            abertura=101.0,
            data=datetime.now(), # Aceita apenas datetime!
            maximo=101.0,
            minimo=101.0,
            fechamento=101.0,
            volume=101.0
        )
        db.session.add(cotacoes)
        db.session.commit()

        self.assertEqual(Cotacao.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Testa a home (que não precisa de login)
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Testa a página login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Testa a rota logout, inacessível sem a login
        e redireciona para a pagina de login e depois logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_painel_view(self):
        """
        Testa painel não acessível 
        e redireciona para login
        """
        target_url = url_for('home.painel')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_empresas_view(self):
        """
        Listar empresas é inacessível sem login
        redireciona para o login e depois para empresas
        """
        target_url = url_for('home.listar_empresas')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_cotacoes_view(self):
        """
        testa a pagina de cotacoes que é inacessível
        sem login e redireciona para login e depois ela novamente
        """
        target_url = url_for('home.listar_cotacoes')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_usuarios_view(self):
        """"
        testa a pagina de cotacoes que é inacessível
        sem login e redireciona para login e depois ela novamente
        """
        target_url = url_for('home.listar_usuarios')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


if __name__ == '__main__':
    unittest.main()
