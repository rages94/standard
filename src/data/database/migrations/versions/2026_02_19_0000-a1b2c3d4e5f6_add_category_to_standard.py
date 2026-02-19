"""add category to standard

Revision ID: a1b2c3d4e5f6
Revises: 5cd33ad44be8
Create Date: 2026-02-19 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "5cd33ad44be8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("standard", sa.Column("category", sa.String(), nullable=True))
    op.create_index(
        op.f("ix_standard_category"), "standard", ["category"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_standard_category"), table_name="standard")
    op.drop_column("standard", "category")
