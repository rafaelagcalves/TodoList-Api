"""empty message

Revision ID: 6d78ddaf9e3d
Revises: 76adb6494f4b
Create Date: 2021-02-10 16:14:22.934923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d78ddaf9e3d'
down_revision = '76adb6494f4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'tasks', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    # ### end Alembic commands ###
