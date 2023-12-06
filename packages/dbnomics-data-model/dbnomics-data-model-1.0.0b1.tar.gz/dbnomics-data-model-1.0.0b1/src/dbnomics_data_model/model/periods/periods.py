from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from functools import cached_property
from typing import Self, cast

from isoweek import Week
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.formatters import format_month_num, format_week_num, format_year_num

__all__ = [
    "BimesterPeriod",
    "DayPeriod",
    "MonthPeriod",
    "Period",
    "QuarterPeriod",
    "SemesterPeriod",
    "WeekPeriod",
    "YearPeriod",
]


class PeriodType(Enum):
    """Type of the period assigned to each Period sub-class instance in order to identify serialized values."""

    BIMESTER = "bimester"
    DAY = "day"
    MONTH = "month"
    QUARTER = "quarter"
    SEMESTER = "semester"
    WEEK = "week"
    YEAR = "year"


@dataclass(frozen=True, order=True)
class Period(ABC):
    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            period = cast(Self, parsers.period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return period

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractproperty
    def first_day(self) -> date:
        pass


@dataclass(frozen=True, order=True)
class BimesterPeriod(Period):
    """A period of 2 consecutive months."""

    year_num: int
    bimester_num: int

    type: PeriodType = field(default=PeriodType.BIMESTER, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            bimester_period = cast(Self, parsers.bimester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return bimester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-B{self.bimester_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.bimester_num * 2 - 1


@dataclass(frozen=True, order=True)
class DayPeriod(Period):
    year_num: int
    month_num: int
    day_num: int

    type: PeriodType = field(default=PeriodType.DAY, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            day_period = cast(Self, parsers.day_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return day_period

    def __str__(self) -> str:
        return self.first_day.isoformat()

    @cached_property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, self.day_num)


@dataclass(frozen=True, order=True)
class MonthPeriod(Period):
    year_num: int
    month_num: int

    type: PeriodType = field(default=PeriodType.MONTH, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            month_period = cast(Self, parsers.month_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return month_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-{format_month_num(self.month_num)}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, 1)


@dataclass(frozen=True, order=True)
class QuarterPeriod(Period):
    year_num: int
    quarter_num: int

    type: PeriodType = field(default=PeriodType.QUARTER, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            quarter_period = cast(Self, parsers.quarter_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return quarter_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-Q{self.quarter_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.quarter_num * 3 - 2


@dataclass(frozen=True, order=True)
class SemesterPeriod(Period):
    """A period of 6 consecutive months."""

    year_num: int
    semester_num: int

    type: PeriodType = field(default=PeriodType.SEMESTER, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            semester_period = cast(Self, parsers.semester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return semester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-S{self.semester_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.semester_num * 6 - 5


@dataclass(frozen=True, order=True)
class WeekPeriod(Period):
    year_num: int
    week_num: int

    type: PeriodType = field(default=PeriodType.WEEK, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            week_period = cast(Self, parsers.week_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return week_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-W{format_week_num(self.week_num)}"

    @property
    def first_day(self) -> date:
        return cast(date, self._week.monday())

    @cached_property
    def _week(self) -> Week:
        return Week(self.year_num, self.week_num)


@dataclass(frozen=True, order=True)
class YearPeriod(Period):
    year_num: int

    type: PeriodType = field(default=PeriodType.YEAR, init=False)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            year_period = cast(Self, parsers.year_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return year_period

    def __str__(self) -> str:
        return str(self.year_num)

    @property
    def first_day(self) -> date:
        return date(self.year_num, 1, 1)
