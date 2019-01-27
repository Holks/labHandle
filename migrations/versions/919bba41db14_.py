"""empty message

Revision ID: 919bba41db14
Revises: 754c8852714b
Create Date: 2019-01-25 00:52:05.263198

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '919bba41db14'
down_revision = '754c8852714b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instrument',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mois_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instrument_mois_id'), 'instrument', ['mois_id'], unique=True)
    op.create_table('workstation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=200), nullable=True),
    sa.Column('designation', sa.String(length=200), nullable=True),
    sa.Column('responsible_user_id', sa.Integer(), nullable=True),
    sa.Column('instruments', sa.Integer(), nullable=True),
    sa.Column('version', sa.String(length=200), nullable=False),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('approved', sa.DateTime(), nullable=True),
    sa.Column('last_reviewed', sa.DateTime(), nullable=True),
    sa.Column('next_reviewed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instruments'], ['user.id'], ),
    sa.ForeignKeyConstraint(['responsible_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    op.create_table('workstation_instruments',
    sa.Column('instrument_id', sa.Integer(), nullable=True),
    sa.Column('workstation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instrument.id'], ),
    sa.ForeignKeyConstraint(['workstation_id'], ['workstation.id'], )
    )
    op.add_column('document', sa.Column('approved', sa.DateTime(), nullable=True))
    op.add_column('document', sa.Column('description', sa.String(length=200), nullable=True))
    op.add_column('document', sa.Column('last_reviewed', sa.DateTime(), nullable=True))
    op.add_column('document', sa.Column('next_reviewed', sa.DateTime(), nullable=True))
    op.drop_column('document', 'reviewed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('reviewed', mysql.DATETIME(), nullable=True))
    op.drop_column('document', 'next_reviewed')
    op.drop_column('document', 'last_reviewed')
    op.drop_column('document', 'description')
    op.drop_column('document', 'approved')
    op.drop_table('workstation_instruments')
    op.drop_table('workstation')
    op.drop_index(op.f('ix_instrument_mois_id'), table_name='instrument')
    op.drop_table('instrument')
    # ### end Alembic commands ###