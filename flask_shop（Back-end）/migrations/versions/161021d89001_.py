"""empty message

Revision ID: 161021d89001
Revises: e9fcdd60a65a
Create Date: 2020-05-03 17:41:31.191667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161021d89001'
down_revision = 'e9fcdd60a65a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_order',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('pay_status', sa.Integer(), nullable=True),
    sa.Column('is_send', sa.Integer(), nullable=True),
    sa.Column('fapiao_title', sa.String(length=32), nullable=True),
    sa.Column('fapiao_company', sa.String(length=128), nullable=True),
    sa.Column('fapiao_content', sa.String(length=521), nullable=True),
    sa.Column('addrs', sa.String(length=521), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_express',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=64), nullable=True),
    sa.Column('update_time', sa.String(length=32), nullable=True),
    sa.Column('oid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['oid'], ['t_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_order_detail',
    sa.Column('gid', sa.Integer(), nullable=False),
    sa.Column('oid', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['gid'], ['t_goods.id'], ),
    sa.ForeignKeyConstraint(['oid'], ['t_order.id'], ),
    sa.PrimaryKeyConstraint('gid', 'oid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_order_detail')
    op.drop_table('t_express')
    op.drop_table('t_order')
    # ### end Alembic commands ###
