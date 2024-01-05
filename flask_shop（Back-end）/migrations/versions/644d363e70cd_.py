"""empty message

Revision ID: 644d363e70cd
Revises: 965e7b1ea9b4
Create Date: 2020-04-20 00:39:57.502897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '644d363e70cd'
down_revision = '965e7b1ea9b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_attribute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('val', sa.String(length=255), nullable=True),
    sa.Column('_type', sa.Enum('static', 'dynamic'), nullable=True),
    sa.Column('cid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['t_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_attribute')
    # ### end Alembic commands ###
