from enum import Enum


class RarityType(str, Enum):
    """Редкость достижения"""

    COMMON = "common"  # 100
    RARE = "rare"  # 1000
    EPIC = "epic"  # 10000
    LEGENDARY = "legendary"  # Особые


class ConditionType(str, Enum):
    """Тип условия для получения достижения"""

    COUNT = "count"  # Количество повторений
    WEIGHT = "weight"  # Суммарный вес (count * weight)
    STREAK = "streak"  # Серия дней подряд
    META = "meta"  # Получение других достижений


class TimePeriod(str, Enum):
    """Период времени для подсчёта"""

    TOTAL = "total"  # За всё время
    DAILY = "daily"  # За день
    MONTHLY = "monthly"  # За месяц


class MetaTier(str, Enum):
    """Уровень мета-достижения (для явного определения вместо парсинга имени)"""

    BEGINNER = "beginner"  # Начинающий (100 повторений/вес)
    ATHLETE = "athlete"  # Спортсмен (1000 повторений/вес)
    MASTER = "master"  # Мастер (10000 повторений/вес)
    LEGEND = "legend"  # Легенда (все достижения)


class AchievementCategory(str, Enum):
    """Категории достижений по упражнениям"""

    # Упражнения со своим весом
    PUSHUPS = "pushups"  # Отжимания
    PULLUPS = "pullups"  # Подтягивания
    SQUATS = "squats"  # Приседания
    CRUNCHES = "crunches"  # Скручивания
    RUNNING = "running"  # Бег (км)
    DIPS = "dips"  # Отжимания на брусьях
    ABS = "abs"  # Пресс
    ABS_DIPS = "abs_dips"  # Пресс на брусьях
    JUMP_ROPE = "jump_rope"  # Скакалка
    PLANK = "plank"  # Планка (мин)
    BURPEES = "burpees"  # Бёрпи
    CALVES = "calves"  # Икры (поднятия на носки)

    # Тяжёлая атлетика
    BENCH_PRESS = "bench_press"  # Жим штанги лёжа
    WEIGHTED_SQUATS = "weighted_squats"  # Приседание со штангой
    DEADLIFT = "deadlift"  # Становая тяга
    BICEPS_CURL = "biceps_curl"  # Подъём штанги на бицепс
    WEIGHTED_PULLUPS = "weighted_pullups"  # Подтягивания с весом
    WEIGHTED_DIPS = "weighted_dips"  # Отжимания на брусьях с весом

    # Специальные категории
    STREAK = "streak"  # Серии дней
    META = "meta"  # Мета-достижения
