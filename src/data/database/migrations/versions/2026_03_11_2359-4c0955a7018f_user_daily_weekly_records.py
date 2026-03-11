"""user_daily_weekly_records

Revision ID: 4c0955a7018f
Revises: f9936941217b
Create Date: 2026-03-11 23:59:35.081337

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4c0955a7018f'
down_revision: Union[str, None] = 'f9936941217b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('max_daily_norm', sa.Float(), server_default='0', nullable=False))
    op.add_column('user', sa.Column('max_weekly_norm', sa.Float(), server_default='0', nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'max_weekly_norm')
    op.drop_column('user', 'max_daily_norm')
