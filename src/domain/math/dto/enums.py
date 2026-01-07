from enum import Enum


class ExerciseEnum(str, Enum):
    deadlift = 'Становая тяга'
    squats = 'Присед со штангой'
    bench_press = 'Жим лежа'
    biceps_curl = 'Подъем штанги на бицепс'
    dips_on_bars = 'Отжимания на брусьях с отягощением'
    pull_ups = 'Подтягивания с отягощением'


class SexEnum(str, Enum):
    male = 'male'
    female = 'female'
