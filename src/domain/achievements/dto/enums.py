from enum import StrEnum


class RarityType(StrEnum):
    """Редкость достижения"""

    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class ConditionType(StrEnum):
    """Тип условия для получения достижения"""

    COUNT = "count"
    WEIGHT = "weight"
    STREAK = "streak"
    META = "meta"


class TimePeriod(StrEnum):
    """Период времени для подсчёта"""

    TOTAL = "total"
    DAILY = "daily"
    MONTHLY = "monthly"


class MetaTier(StrEnum):
    """Уровень мета-достижения (для явного определения вместо парсинга имени)"""

    BEGINNER = "beginner"
    ATHLETE = "athlete"
    MASTER = "master"
    LEGEND = "legend"


class AchievementCategory(StrEnum):
    """Категории достижений по упражнениям"""

    PUSHUPS = "Отжимания"
    PULLUPS = "Подтягивания"
    SQUATS = "Приседания"
    CRUNCHES = "Скручивания"
    RUNNING = "Бег"
    DIPS = "Отжимания на брусьях"
    ABS = "Пресс"
    ABS_DIPS = "Пресс на брусьях"
    JUMP_ROPE = "Скакалка"
    PLANK = "Планка"
    BURPEES = "Бёрпи"
    CALVES = "Поднятия на носки"

    BENCH_PRESS = "Жим штанги лёжа"
    WEIGHTED_SQUATS = "Приседания со штангой"
    DEADLIFT = "Становая тяга"
    BICEPS_CURL = "Подъём штанги на бицепс"
    WEIGHTED_PULLUPS = "Подтягивания с отягощением"
    WEIGHTED_DIPS = "Отжимания на брусьях с отягощением"

    STREAK = "Серии дней"
    META = "Мета-достижения"
