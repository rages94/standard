"""user_completed_type

Revision ID: aa3051a06890
Revises: 75d9e8b70de9
Create Date: 2024-12-28 23:51:12.751751

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa3051a06890'
down_revision: Union[str, None] = '75d9e8b70de9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('completed_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'completed_type')
    # ### end Alembic commands ###