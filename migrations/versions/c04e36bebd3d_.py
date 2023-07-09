"""empty message

Revision ID: c04e36bebd3d
Revises: 7a5ff6c5f971
Create Date: 2023-07-09 18:05:40.467849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04e36bebd3d'
down_revision = '7a5ff6c5f971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('garage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('garage', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
