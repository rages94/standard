"""add_is_viewed_to_user_achievement

Revision ID: c33045bcae27
Revises: 4c0955a7018f
Create Date: 2026-03-24 18:37:52.029018

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c33045bcae27"
down_revision: Union[str, None] = "4c0955a7018f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_achievement",
        sa.Column("is_viewed", sa.Boolean(), nullable=False, server_default="false"),
    )


def downgrade() -> None:
    op.drop_column("user_achievement", "is_viewed")
