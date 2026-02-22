from enum import Enum


class ExerciseEnum(str, Enum):
    deadlift = "Становая тяга"
    squats = "Приседания со штангой"
    bench_press = "Жим штанги лёжа"
    biceps_curl = "Подъём штанги на бицепс"
    dips_on_bars = "Отжимания на брусьях с отягощением"
    pull_ups = "Подтягивания с отягощением"


class SexEnum(str, Enum):
    male = "male"
    female = "female"
