from pathlib import Path
from typing import cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData
from dbnomics_data_model.validation.errors.validation_error_level import ValidationErrorLevel

STO001 = ValidationErrorCodeRegistry.request("STO001")


class TsvError(DataModelError):
    pass


class TsvHeaderWriteError(TsvError):
    def __init__(self, fieldnames: list[str], file_path: Path) -> None:
        msg = f"Could not write TSV header to {file_path}"
        super().__init__(msg=msg)
        self.fieldnames = fieldnames
        self.file_path = file_path


class TsvRowWriteError(TsvError):
    def __init__(self, file_path: Path, row: dict[str, str]) -> None:
        msg = f"Could not write TSV row to {file_path}"
        super().__init__(msg=msg)
        self.row = row
        self.file_path = file_path


class InvalidTsvObservationHeader(TsvError):
    def __init__(self, header: list[str]) -> None:
        msg = f"Invalid TSV file header: {header!r}"
        super().__init__(msg=msg)
        self.header = header

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        header_json = cast(Json, self.header)
        return ValidationErrorData(
            code=STO001,
            extra={"header": header_json},
            level=ValidationErrorLevel.ERROR,
            path=None,
        )


class InvalidTsvObservationValue(TsvError):
    pass
