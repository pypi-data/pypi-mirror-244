import re
from typing import Final, Self

from phantom.re import FullMatch

validation_error_code_re: Final = re.compile(r"(CT|D|DJ|DR|P|SO|STO)\d{3}")


class ValidationErrorCode(FullMatch, pattern=validation_error_code_re):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        return super().parse(value)
