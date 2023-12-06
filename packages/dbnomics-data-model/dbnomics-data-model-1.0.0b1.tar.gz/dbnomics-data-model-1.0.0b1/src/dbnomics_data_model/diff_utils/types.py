from collections.abc import Sequence
from enum import Enum
from typing import Final, TypeAlias

ChangePath: TypeAlias = Sequence[int | tuple[int, int] | str]


class ChangeType(Enum):
    ADD = "A"
    DELETE = "D"
    MODIFY = "M"


FieldName: TypeAlias = str


class Missing:
    def __rich__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "-"


# Sentinel value
MISSING: Final = Missing()
