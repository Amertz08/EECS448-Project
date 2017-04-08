"""empty message

Revision ID: de77beb7eece
Revises: 
Create Date: 2017-04-08 17:13:13.135371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de77beb7eece'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('city', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('state', sa.String(length=2), nullable=True))
    op.add_column('users', sa.Column('zip', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'zip')
    op.drop_column('users', 'state')
    op.drop_column('users', 'city')
    # ### end Alembic commands ###