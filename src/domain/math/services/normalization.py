from functools import cache

import numpy as np
from scipy.optimize import curve_fit

from src.domain.math.dto.enums import ExerciseEnum, SexEnum
from src.domain.math.dto.inner import CoordinateCalibration


class BaseNormalization:
    wilks_2020_coeffs = {
        SexEnum.male: {
            "a": -216.0475144,
            "b": 16.2606339,
            "c": -0.002388645,
            "d": -0.00113732,
            "e": 7.01863e-06,
            "f": -1.291e-08,
        },
        SexEnum.female: {
            "a": 594.31747775582,
            "b": -27.23842536447,
            "c": 0.82112226871,
            "d": -0.00930733913,
            "e": 4.731582e-05,
            "f": -9.054e-08,
        },
    }

    @classmethod
    def power_func(cls, x: float, a: float, p: float, h: float) -> float:
        return a * np.power(x, p) + h

    @classmethod
    def lin_func(cls, x: float, p: float, h: float) -> float:
        return np.power(x, p) + h

    @classmethod
    def wilks_2020_func(cls, body_weight: float, lift_weight: float, sex: SexEnum) -> float:
        sex = sex.lower()
        if sex not in cls.wilks_2020_coeffs:
            raise ValueError("sex must be 'male' or 'female'")
        c = cls.wilks_2020_coeffs[sex]
        denom = (
                c["a"]
                + c["b"] * body_weight
                + c["c"] * (body_weight ** 2)
                + c["d"] * (body_weight ** 3)
                + c["e"] * (body_weight ** 4)
                + c["f"] * (body_weight ** 5)
        )
        return 500 * lift_weight / denom

    @classmethod
    def get_func_params(cls, xs: list[float], ys: list[float]) -> tuple[float, float]:
        params, _ = curve_fit(cls.power_func, xs, ys)
        return params


class ExerciseNormalizationService(BaseNormalization):
    exercise_calibration_map: dict[ExerciseEnum, CoordinateCalibration] = {
        ExerciseEnum.bench_press: CoordinateCalibration(
            xs=[110, 96, 84, 75, 68, 59, 0],
            ys=[25, 17, 13, 10, 8, 5, 0]
        ),
        ExerciseEnum.deadlift: CoordinateCalibration(
            xs=[169, 148, 130, 114, 105, 91, 0],
            ys=[25, 17, 13, 10, 8, 5, 0]
        ),
        ExerciseEnum.squats: CoordinateCalibration(
            xs=[158.5, 137, 119, 103, 94.5, 80, 0],
            ys=[25, 17, 13, 10, 8, 5, 0.23]
        ),
        ExerciseEnum.biceps_curl: CoordinateCalibration(
            xs=[51.5, 44.5, 39, 34, 28.5, 25, 0],
            ys=[25, 17, 13, 10, 8, 5, 0]
        ),
        ExerciseEnum.dips_on_bars: CoordinateCalibration(
            xs=[80, 67.5, 59, 51.5, 44.5, 39, 0],
            ys=[25, 17, 13, 10, 8, 5, 0.5]
        ),
        ExerciseEnum.pull_ups: CoordinateCalibration(
            xs=[55, 48, 43, 37.5, 30, 26.5, 0],
            ys=[23, 20, 17, 14, 11, 7, 1.2]
        ),
    }

    @classmethod
    @cache
    def _get_exercise_params(cls, exercise: ExerciseEnum) -> tuple[float, float]:
        coordinate_calibration = cls.exercise_calibration_map[exercise]
        return cls.get_func_params(coordinate_calibration.xs, coordinate_calibration.ys)

    @classmethod
    def normalization(
        cls,
        body_weight: float,
        lift_weight: float,
        exercise: ExerciseEnum,
        sex: SexEnum = SexEnum.male,
    ) -> float:
        wilks_coef = cls.wilks_2020_func(body_weight, lift_weight, sex)
        params = cls._get_exercise_params(exercise)
        return round(cls.power_func(wilks_coef, *params), 2)

