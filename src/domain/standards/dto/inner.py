from pydantic import BaseModel

from src.data.models import Standard
from src.domain.standards.dto.enums import ExerciseType


class StandardUserRecordSchema(BaseModel):
    standard: Standard
    type: ExerciseType
    count: int | None = None
    weight: float | None = None
