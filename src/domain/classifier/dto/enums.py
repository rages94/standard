from enum import Enum


class TextClass(Enum):
    completed_standards = "completed_standards"
    total_liabilities = "total_liabilities"
    liability = "liability"
    standard_history = "standard_history"
    liability_history = "liability_history"
    credit_history = "credit_history"
    rating = "rating"
    other = "other"
