from enum import Enum

__all__ = ["FrequencyCode", "FrequencyLabel"]


# TODO maybe replace enums by a proper domain-level class


class FrequencyCode(Enum):
    ANNUAL = "A"
    BIMESTRIAL = "B"
    DAILY = "D"
    MONTHLY = "M"
    QUARTERLY = "Q"
    SEMESTRIAL = "S"
    WEEKLY = "W"


class FrequencyLabel(Enum):
    ANNUAL = "Annual"
    BIMESTRIAL = "Bimestrial"
    DAILY = "Daily"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    SEMESTRIAL = "Semestrial"
    WEEKLY = "Weekly"
