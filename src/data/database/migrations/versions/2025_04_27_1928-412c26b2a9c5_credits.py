"""credits

Revision ID: 412c26b2a9c5
Revises: c7ab5d7d8c8f
Create Date: 2025-04-27 19:28:59.624019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '412c26b2a9c5'
down_revision: Union[str, None] = 'c7ab5d7d8c8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('credit',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('completed_count', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('deadline_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('credit')
    # ### end Alembic commands ###
