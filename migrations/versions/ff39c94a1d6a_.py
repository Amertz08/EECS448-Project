"""empty message

Revision ID: ff39c94a1d6a
Revises: 
Create Date: 2017-04-21 16:18:40.761667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff39c94a1d6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.Column('country', sa.String(length=32), nullable=True),
    sa.Column('place_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_places')
    # ### end Alembic commands ###
