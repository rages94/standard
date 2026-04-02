"""user_records

Revision ID: a4de9ceaad98
Revises: c33045bcae27
Create Date: 2026-03-25 21:47:54.566459

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a4de9ceaad98"
down_revision: Union[str, None] = "c33045bcae27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column("count", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute("""
               INSERT INTO user_records (id, user_id, type, count, created_at)
               SELECT gen_random_uuid(), id, 'daily', max_daily_norm, now()
               FROM "user"
               WHERE max_daily_norm > 0
               """)

    op.execute("""
               INSERT INTO user_records (id, user_id, type, count, created_at)
               SELECT gen_random_uuid(), id, 'weekly', max_weekly_norm, now()
               FROM "user"
               WHERE max_weekly_norm > 0
               """)

    op.drop_column("user", "max_weekly_norm")
    op.drop_column("user", "max_daily_norm")


def downgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "max_daily_norm",
            sa.DOUBLE_PRECISION(precision=53),
            server_default=sa.text("'0'::double precision"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "max_weekly_norm",
            sa.DOUBLE_PRECISION(precision=53),
            server_default=sa.text("'0'::double precision"),
            autoincrement=False,
            nullable=False,
        ),
    )

    op.execute("""
        UPDATE "user"
        SET max_daily_norm = COALESCE((
            SELECT count FROM user_records 
            WHERE user_records.user_id = "user".id AND type = 'daily'
            ORDER BY created_at DESC LIMIT 1
        ), 0)
    """)

    op.execute("""
        UPDATE "user"
        SET max_weekly_norm = COALESCE((
            SELECT count FROM user_records 
            WHERE user_records.user_id = "user".id AND type = 'weekly'
            ORDER BY created_at DESC LIMIT 1
        ), 0)
    """)

    op.drop_table("userrecord")
