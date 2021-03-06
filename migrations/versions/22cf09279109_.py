"""empty message

Revision ID: 22cf09279109
Revises: 
Create Date: 2019-02-10 11:04:24.511933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22cf09279109'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('designation', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('designation')
    )
    op.create_index(op.f('ix_department_location'), 'department', ['location'], unique=False)
    op.create_index(op.f('ix_department_name'), 'department', ['name'], unique=False)
    op.create_table('documentcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documentcategory_name'), 'documentcategory', ['name'], unique=False)
    op.create_table('documentstatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documentstatus_status'), 'documentstatus', ['status'], unique=False)
    op.create_table('instrument',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mois_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('data_fields_json', sa.Text(), nullable=True),
    sa.Column('last_maintenance_date', sa.DateTime(), nullable=True),
    sa.Column('last_maintenance_interval', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instrument_description'), 'instrument', ['description'], unique=False)
    op.create_index(op.f('ix_instrument_mois_id'), 'instrument', ['mois_id'], unique=True)
    op.create_table('taskcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_taskcategory_name'), 'taskcategory', ['name'], unique=False)
    op.create_table('usercategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usercategory_name'), 'usercategory', ['name'], unique=True)
    op.create_table('userstatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userstatus_status'), 'userstatus', ['status'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['usercategory.id'], ),
    sa.ForeignKeyConstraint(['status'], ['userstatus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('association_dep',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('deparment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deparment_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('designation', sa.String(length=100), nullable=False),
    sa.Column('file', sa.String(length=500), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('uploader_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('reviwer_id', sa.Integer(), nullable=True),
    sa.Column('version', sa.String(length=200), nullable=False),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('approver_id', sa.Integer(), nullable=True),
    sa.Column('approved', sa.DateTime(), nullable=True),
    sa.Column('last_reviewed', sa.DateTime(), nullable=True),
    sa.Column('next_reviewed', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['approver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['documentcategory.id'], ),
    sa.ForeignKeyConstraint(['reviwer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status'], ['documentstatus.id'], ),
    sa.ForeignKeyConstraint(['uploader_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    op.create_index(op.f('ix_document_designation'), 'document', ['designation'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_name'), 'notification', ['name'], unique=False)
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('addded_date', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('adder_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adder_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=False)
    op.create_table('uncertainty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=200), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('reviewed', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('reviwer_id', sa.Integer(), nullable=True),
    sa.Column('version', sa.String(length=200), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('designation', sa.String(length=100), nullable=True),
    sa.Column('instrument', sa.String(length=100), nullable=True),
    sa.Column('subfield', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['documentcategory.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['reviwer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status'], ['documentstatus.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    op.create_index(op.f('ix_uncertainty_designation'), 'uncertainty', ['designation'], unique=False)
    op.create_index(op.f('ix_uncertainty_instrument'), 'uncertainty', ['instrument'], unique=False)
    op.create_table('workstation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=200), nullable=True),
    sa.Column('designation', sa.String(length=200), nullable=True),
    sa.Column('scope', sa.String(length=200), nullable=True),
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
    op.create_table('association_unc',
    sa.Column('uncertainty_id', sa.Integer(), nullable=True),
    sa.Column('deparment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deparment_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['uncertainty_id'], ['uncertainty.id'], )
    )
    op.create_table('workstation_instruments',
    sa.Column('instrument_id', sa.Integer(), nullable=True),
    sa.Column('workstation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instrument.id'], ),
    sa.ForeignKeyConstraint(['workstation_id'], ['workstation.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workstation_instruments')
    op.drop_table('association_unc')
    op.drop_table('workstation')
    op.drop_index(op.f('ix_uncertainty_instrument'), table_name='uncertainty')
    op.drop_index(op.f('ix_uncertainty_designation'), table_name='uncertainty')
    op.drop_table('uncertainty')
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_index(op.f('ix_notification_name'), table_name='notification')
    op.drop_table('notification')
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_document_designation'), table_name='document')
    op.drop_table('document')
    op.drop_table('association_dep')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_userstatus_status'), table_name='userstatus')
    op.drop_table('userstatus')
    op.drop_index(op.f('ix_usercategory_name'), table_name='usercategory')
    op.drop_table('usercategory')
    op.drop_index(op.f('ix_taskcategory_name'), table_name='taskcategory')
    op.drop_table('taskcategory')
    op.drop_index(op.f('ix_instrument_mois_id'), table_name='instrument')
    op.drop_index(op.f('ix_instrument_description'), table_name='instrument')
    op.drop_table('instrument')
    op.drop_index(op.f('ix_documentstatus_status'), table_name='documentstatus')
    op.drop_table('documentstatus')
    op.drop_index(op.f('ix_documentcategory_name'), table_name='documentcategory')
    op.drop_table('documentcategory')
    op.drop_index(op.f('ix_department_name'), table_name='department')
    op.drop_index(op.f('ix_department_location'), table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###
