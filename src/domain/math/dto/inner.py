from pydantic import BaseModel


class CoordinateCalibration(BaseModel):
    xs: list[float | int]
    ys: list[float | int]
