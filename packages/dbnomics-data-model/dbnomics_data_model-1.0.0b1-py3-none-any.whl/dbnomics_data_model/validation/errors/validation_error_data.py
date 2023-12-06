from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias, cast

from jsonalias import Json

from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode
from dbnomics_data_model.validation.errors.validation_error_level import ValidationErrorLevel

if TYPE_CHECKING:
    from dbnomics_data_model.json_utils import JsonObject

ValidationErrorPath: TypeAlias = list[tuple[str, str]]


@dataclass(kw_only=True)
class ValidationErrorData:
    code: ValidationErrorCode | None
    extra: "JsonObject | None" = None
    level: ValidationErrorLevel
    path: ValidationErrorPath | None

    def to_json(self) -> "JsonObject":
        result: "JsonObject" = {"level": self.level.value}

        if self.code is not None:
            result["code"] = self.code

        if self.extra:
            result["extra"] = self.extra

        if self.path is not None:
            result["path"] = cast(Json, self.path)

        return result
