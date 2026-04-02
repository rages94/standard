"""daily_stats

Revision ID: d1e2f3a4b5c6
Revises: a4de9ceaad98
Create Date: 2026-04-02 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1e2f3a4b5c6"
down_revision: Union[str, None] = "a4de9ceaad98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "daily_stats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_count", sa.Float(), nullable=False, server_default="0"),
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
        sa.UniqueConstraint("user_id", "date", name="uq_daily_stats_user_date"),
    )

    op.execute("""
        INSERT INTO daily_stats (id, user_id, date, total_count, created_at, updated_at)
        SELECT 
            gen_random_uuid(),
            user_id,
            created_at::date,
            SUM(COALESCE(total_norm, 0)),
            now(),
            now()
        FROM completed_standard
        WHERE total_norm IS NOT NULL AND total_norm > 0
        GROUP BY user_id, created_at::date
    """)

    op.execute("""
        INSERT INTO user_records (id, user_id, type, count, created_at, updated_at)
        SELECT 
            gen_random_uuid(),
            user_id,
            'daily',
            MAX(total_count),
            now(),
            now()
        FROM daily_stats
        GROUP BY user_id
        HAVING MAX(total_count) > 0
    """)

    op.execute("""
        INSERT INTO user_records (id, user_id, type, count, created_at, updated_at)
        SELECT 
            gen_random_uuid(),
            user_id,
            'weekly',
            MAX(week_total),
            now(),
            now()
        FROM (
            SELECT 
                user_id,
                date_trunc('week', date)::date AS week_start,
                SUM(total_count) AS week_total
            FROM daily_stats
            GROUP BY user_id, date_trunc('week', date)
        ) weekly_sums
        GROUP BY user_id
        HAVING MAX(week_total) > 0
    """)


def downgrade() -> None:
    op.execute("DELETE FROM user_records")
    op.drop_table("daily_stats")
