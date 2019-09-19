from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from app import db
from app.models import Usuario 


@auth.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(email=form.email.data,
                            login=form.user.data,
                            nome=form.nome.data,
                            sobrenome=form.sobrenome.data,
                            password=form.senha.data)

        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login abaixo.')

        return redirect(url_for('auth.login'))

    return render_template('auth/cadastro.html', form=form, title='Cadastrar')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = Usuario.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(
                form.senha.data):
            login_user(user)

            return redirect(url_for('home.painel'))

        else:
            flash('Usuário ou senha inválidos.')

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta!')

    return redirect(url_for('auth.login'))

