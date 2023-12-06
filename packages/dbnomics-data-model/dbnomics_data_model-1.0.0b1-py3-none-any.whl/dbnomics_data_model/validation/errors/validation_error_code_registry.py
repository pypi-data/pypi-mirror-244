from typing import ClassVar

from .validation_error_code import ValidationErrorCode


class ValidationErrorCodeRegistry:
    _requested_error_codes: ClassVar[set[ValidationErrorCode]] = set()

    @classmethod
    def request(cls, value: str) -> ValidationErrorCode:
        error_code = ValidationErrorCode.parse(value)
        if error_code in cls._requested_error_codes:
            msg = f"Error code {error_code} was already requested"
            raise ValueError(msg)

        cls._requested_error_codes.add(error_code)
        return error_code
