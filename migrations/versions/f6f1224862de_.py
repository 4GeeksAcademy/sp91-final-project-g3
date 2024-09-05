"""empty message

Revision ID: f6f1224862de
Revises: d79c87bc0938
Create Date: 2024-09-05 11:26:12.355219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f1224862de'
down_revision = 'd79c87bc0938'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('programador', schema=None) as batch_op:
        batch_op.alter_column('rating_value',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('programador', schema=None) as batch_op:
        batch_op.alter_column('rating_value',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    # ### end Alembic commands ###
