"""empty message

Revision ID: 918a329faf46
Revises: 
Create Date: 2023-03-07 19:34:11.826768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '918a329faf46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('objects', sa.Column('cls', sa.TEXT(), nullable=True))
    op.add_column('worlds', sa.Column('owner', sa.TEXT(), nullable=True))
    op.add_column('worlds', sa.Column('private', sa.BOOLEAN(), nullable=True))
    op.add_column('worlds', sa.Column('name', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('worlds', 'name')
    op.drop_column('worlds', 'private')
    op.drop_column('worlds', 'owner')
    op.drop_column('objects', 'cls')
    # ### end Alembic commands ###