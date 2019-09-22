from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField, PasswordField, \
                    DateTimeField
from wtforms.validators import DataRequired, EqualTo
from datetime import datetime

class CotaForm(FlaskForm):
    dt = DateField('Data da cotação', validators=[DataRequired()], default=datetime.utcnow)
    submit = SubmitField('Enviar')

class EditarCotacaoForm(FlaskForm):
    dt = StringField('Data do cadastro', validators=[DataRequired()])
    abertura = FloatField('Valor de abertura', validators=[DataRequired()])
    maximo = FloatField('Valor máximo', validators=[DataRequired()]) 
    minimo = FloatField('Valor mínimo', validators=[DataRequired()]) 
    fechamento = FloatField('Valor de fechamento', validators=[DataRequired()]) 
    volume = FloatField('Volume', validators=[DataRequired()]) 

    submit = SubmitField('Enviar')

class EmpresaForm(FlaskForm):
    sigla = StringField('sigla da empresa', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class EditarEmpresaForm(FlaskForm):
    nome = StringField('Nome da empresa', validators=[DataRequired()])
    simbolo = StringField('Símbolo da empresa', validators=[DataRequired()] )
    regiao = StringField('Região', validators=[DataRequired()])
    tipo =StringField('Tipo', validators=[DataRequired()]) 
    abertura =StringField('Abertura', validators=[DataRequired()]) 
    fechamento =StringField('Fechamento', validators=[DataRequired()]) 
    zona =StringField('Zona', validators=[DataRequired()]) 
    moeda =StringField('Moeda', validators=[DataRequired()]) 
    submit = SubmitField('Enviar')

class UsuarioForm(FlaskForm):
    """
    Form para editar configurações do usuário
    """
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirme a senha')
    submit = SubmitField('Cadastrar')
