# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import Usuario


class RegistrationForm(FlaskForm):
    """
    Formulário para criação de novas contas
    """
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    user = StringField('Usuário', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[
                                        DataRequired(),
                                        EqualTo('confirme_senha')
                                        ])
    confirme_senha= PasswordField('Confirme a senha')
    submit = SubmitField('Cadastrar')

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('E-mail já utilizado! Escolha outro.')

    def validate_username(self, field):
        if Usuario.query.filter_by(user=field.data).first():
            raise ValidationError('Usuário já utilizado! Escolha outro.')


class LoginForm(FlaskForm):
    """
    Form de login
    """
    login = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

