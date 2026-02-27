"""calculate_achievements_etc

Revision ID: f9936941217b
Revises: a1b2c3d4e5f6
Create Date: 2026-02-23 22:14:09.571384

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9936941217b"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        update completed_standard cs set total_norm = cs.count / s.count 
        FROM standard s
        WHERE cs.standard_id = s.id 
    """)
    op.execute("""
        update "completed_standard" set user_weight = "user".weight 
        FROM "user" 
        WHERE "completed_standard".user_id = "user".id
     """)

    op.execute("""
        CREATE TEMP TABLE temp_aggregated AS
        SELECT user_id, standard_id, SUM(count) as total_count
        FROM completed_standard
        GROUP BY user_id, standard_id
    """)

    op.execute("""
        CREATE TEMP TABLE temp_achievements AS
        SELECT id, standard_id, target_value 
        FROM achievement 
        WHERE condition_type = 'count' 
        AND standard_id IS NOT NULL 
        AND is_active = true
    """)

    op.execute("""
        INSERT INTO user_achievement_progress (id, user_id, achievement_id, current_value, is_earned, updated_at)
        SELECT gen_random_uuid(), ta.user_id, a.id, ta.total_count, 
               ta.total_count >= a.target_value, NOW()
        FROM temp_achievements a
        JOIN temp_aggregated ta ON a.standard_id = ta.standard_id
    """)

    op.execute("""
        INSERT INTO user_achievement (id, user_id, achievement_id, earned_at, progress_at_earned)
        SELECT gen_random_uuid(), uap.user_id, uap.achievement_id, NOW(), uap.current_value
        FROM user_achievement_progress uap
        JOIN temp_achievements a ON uap.achievement_id = a.id
        WHERE uap.is_earned = true
    """)

    op.execute("DROP TABLE IF EXISTS temp_aggregated")
    op.execute("DROP TABLE IF EXISTS temp_achievements")


def downgrade() -> None:
    pass
