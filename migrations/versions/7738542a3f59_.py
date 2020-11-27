"""empty message

Revision ID: 7738542a3f59
Revises: 
Create Date: 2020-11-27 17:15:55.735992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7738542a3f59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('empresas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('simbolo', sa.String(length=50), nullable=True),
    sa.Column('tipo', sa.String(length=50), nullable=True),
    sa.Column('regiao', sa.String(length=50), nullable=True),
    sa.Column('abertura', sa.String(length=50), nullable=True),
    sa.Column('fechamento', sa.String(length=50), nullable=True),
    sa.Column('zona', sa.String(length=50), nullable=True),
    sa.Column('moeda', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('simbolo')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('login', sa.String(length=60), nullable=True),
    sa.Column('nome', sa.String(length=60), nullable=True),
    sa.Column('sobrenome', sa.String(length=60), nullable=True),
    sa.Column('senha_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_login'), 'usuarios', ['login'], unique=True)
    op.create_index(op.f('ix_usuarios_nome'), 'usuarios', ['nome'], unique=False)
    op.create_index(op.f('ix_usuarios_sobrenome'), 'usuarios', ['sobrenome'], unique=False)
    op.create_index(op.f('ix_usuarios_token'), 'usuarios', ['token'], unique=True)
    op.create_table('cotacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_consulta', sa.DateTime(), nullable=True),
    sa.Column('data_cadastro', sa.DateTime(), nullable=True),
    sa.Column('data_cadastro_string', sa.String(), nullable=True),
    sa.Column('abertura', sa.Float(), nullable=True),
    sa.Column('maximo', sa.Float(), nullable=True),
    sa.Column('minimo', sa.Float(), nullable=True),
    sa.Column('fechamento', sa.Float(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('empresa_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['empresa_id'], ['empresas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cotacoes')
    op.drop_index(op.f('ix_usuarios_token'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_sobrenome'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_nome'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_login'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    op.drop_table('empresas')
    # ### end Alembic commands ###
