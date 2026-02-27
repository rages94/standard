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
