from flask import abort, render_template, redirect, \
     url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required
from config import Config
from . import home
from app import db
import requests, json
from .forms import CotaForm, EditarCotacaoForm, EmpresaForm, EditarEmpresaForm, UsuarioForm
from app.models import Cotacao, Empresa, Usuario
from datetime import datetime

@home.route('/')
def homepage():
    """
    Rende o template na rota /
    """
    return render_template('home/index.html', 
                            title="Bem vindo!")

@home.route('/painel')
@login_required
def painel():
    """
    Rende o painel na rota /painel
    """
    return render_template('home/painel.html', title="Painel")

@home.route('/cotacoes', methods=['GET', 'POST'])
@login_required
def listar_cotacoes():
    page = request.args.get('page', 1, type=int)

    cotacoes = Cotacao.query.order_by(Cotacao.data_cadastro_string.desc()).paginate(
            page, current_app.config['CPP'], False)

    next_url = url_for('home.listar_cotacoes', page=cotacoes.next_num)\
            if cotacoes.has_next else None
    prev_url = url_for('home.listar_cotacoes', page=cotacoes.prev_num)\
            if cotacoes.has_prev else None

    return render_template('home/cotacoes.html',
                           cotacoes=cotacoes.items, 
                           title="Cotações",
                           next_url=next_url,
                           prev_url=prev_url)



@home.route('/cotacoes/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_cotacao():
    cadastrando_cotacao = True
    form = CotaForm()
    if form.validate_on_submit():
        cot = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BOVA11.SAO&apikey=0ED3YY5RQSO6UILH').json()
        cot = cot['Time Series (Daily)'][str(form.dt.data)]
        cotacoes = Cotacao(
            abertura=cot['1. open'],
            data_consulta=form.dt.data,
            maximo=cot['2. high'],
            minimo=cot['3. low'],
            fechamento=cot['4. close'],
            volume=cot['5. volume']
        )
        db.session.add(cotacoes)
        db.session.commit()
        
        flash('Cotação cadastrada com sucesso!')
        return redirect(url_for('home.listar_cotacoes'))

    return render_template("home/cotacao.html", title="Cotações", form=form)

@home.route('/cotacoes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cotacao(id):
    """
    Edita uma cotação diretamente do bd 
    """
    cadastrando_cotacao = False

    cotacao = Cotacao.query.get_or_404(id)
    form = EditarCotacaoForm(obj=cotacao)

    if form.validate_on_submit():
        cotacao.data_cadastro = datetime.strptime(form.dt.data, '%d-%m-%Y')
        cotacao.abertura = form.abertura.data
        cotacao.maximo = form.maximo.data
        cotacao.minimo = form.minimo.data
        cotacao.fechamento = form.fechamento.data
        cotacao.volume = form.volume.data
        db.session.commit()
        flash('Cotação editada com sucesso!')

        return redirect(url_for('home.listar_cotacoes'))

    form.dt.data = cotacao.data_cadastro.strftime("%d-%m-%Y")
    form.abertura.data = cotacao.abertura 
    form.maximo.data = cotacao.maximo
    form.minimo.data = cotacao.minimo
    form.fechamento.data = cotacao.fechamento
    form.volume.data = cotacao.volume


    return render_template('home/cotacao.html', action="Edit",
                           cadastrando_cotacao=cadastrando_cotacao, form=form,
                           cotacao=cotacao, title="Editar cotação")

@home.route('/cotacoes/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def deletar_cotacao(id):
    """
    Deleta uma cotação do banco de dados
    """
    cotacao = Cotacao.query.get_or_404(id)
    
    db.session.delete(cotacao)
    db.session.commit()
    flash('Cotação deletada com sucesso.')

    # redirect to the departments page
    return redirect(url_for('home.listar_cotacoes'))

@home.route('/empresas', methods=['GET', 'POST'])
@login_required
def listar_empresas():
    page = request.args.get('page', 1, type=int)

    empresas = Empresa.query.order_by(Empresa.nome).paginate(
            page, current_app.config['CPP'], False)

    next_url = url_for('home.listar_empresas', page=empresas.next_num)\
            if empresas.has_next else None
    prev_url = url_for('home.listar_empresas', page=empresas.prev_num)\
            if empresas.has_prev else None

    return render_template('home/empresas.html',
                           empresas=empresas.items, 
                           title="Empresas",
                           next_url=next_url,
                           prev_url=prev_url)
        
@home.route('/empresas/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_empresa():
    form = EmpresaForm()
    if form.validate_on_submit():
        try:
            emp = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+ form.sigla.data +'&apikey=0ED3YY5RQSO6UILH').json()
            emp = emp['bestMatches'][0]
        except:
                flash('Nome de empresa inválida! Tente novamente.')
                return redirect(url_for('home.cadastrar_empresa'))
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
        db.session.add(empresa)
        db.session.commit()
        flash('Empresa cadastrada com sucesso!')

        return redirect(url_for('home.listar_empresas'))
    return render_template('home/empresa.html', title="Cadastrar empresa", form=form)

@home.route('/empresas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_empresa(id):
    """
    Edita uma empresa diretamente do bd 
    """
    cadastrando_empresa = False

    empresa = Empresa.query.get_or_404(id)
    form = EditarEmpresaForm(obj=empresa)

    if form.validate_on_submit():
        empresa.nome = form.nome.data
        empresa.simbolo = form.simbolo.data
        empresa.regiao = form.regiao.data
        empresa.tipo = form.tipo.data
        empresa.abertura = form.abertura.data
        empresa.fechamento = form.fechamento.data
        empresa.zona = form.zona.data
        empresa.moeda = form.moeda.data
        db.session.commit()
        flash('Empresa editada com sucesso!')

        return redirect(url_for('home.listar_empresas'))

    form.nome.data = empresa.nome
    form.simbolo.data = empresa.abertura 
    form.regiao.data = empresa.regiao
    form.tipo.data = empresa.tipo
    form.abertura = empresa.abertura
    form.fechamento = empresa.fechamento
    form.zona.data = empresa.zona
    form.moeda.data = empresa.moeda


    return render_template('home/empresa.html', action="Edit",
                           cadastrando_empresa=cadastrando_empresa, form=form,
                           empresa=empresa, title="Editar empresa")

@home.route('/empresas/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def deletar_empresa(id):
    """
    Deleta uma empresa do banco de dados
    """
    empresa = Empresa.query.get_or_404(id)
    
    db.session.delete(empresa)
    db.session.commit()
    flash('Empresa deletada com sucesso.')

    return redirect(url_for('home.listar_empresas'))

@home.route('/usuarios', methods=['GET', 'POST'])
@login_required
def listar_usuarios():

    usuarios = Usuario.query.all()

    return render_template('home/usuarios/usuarios.html',
                           usuarios=usuarios, title="Usuaários")



@home.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_usuarios(id):

    add_usuario = False

    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.sobrenome = form.sobrenome.data
        usuario.password = form.password.data
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário editado com sucesso!')


        return redirect(url_for('home.listar_usuarios'))

    form.nome.data = usuario.nome

    return render_template('home/usuarios/usuario.html', action="Editar",
                           add_usuario=add_usuario, form=form,
                           usuario=usuario, title="Editar Usuário")


@home.route('/usuarios/deletar/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_usuario(id):

    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Funcionário deletado com sucesso!')

    return redirect(url_for('home.listar_usuarios'))

