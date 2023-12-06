import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.annual_rounding_rule import AnnualRoundingRule
from ..models.increment_rule import IncrementRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPaySpineRequest")

@attr.s(auto_attribs=True)
class ContractPaySpineRequest:
    """
    Attributes:
        name (Union[Unset, None, str]): Name of the Pay Spine
        full_time_hours (Union[Unset, float]): Maximum Full Time Hours on this Pay Spine
        full_time_weeks (Union[Unset, float]): Maximum Full Time Weeks on this Pay Spine
        salary_formula (Union[Unset, None, str]): Formula used to derive annual salary
        hourly_divisor (Union[Unset, float]): Hours used to determine Hourly Rate
        hourly_decimals (Union[Unset, int]): Number of decimal places to calculate Hourly Rates
        daily_divisor (Union[Unset, float]): Days used to determine Full time Daily Rate
        daily_decimals (Union[Unset, int]): Number of decimal places to calculate Daily Rates
        annual_decimals (Union[Unset, int]): Number of decimal places to calculate Annual Salaries
        annual_rounding_rule (Union[Unset, AnnualRoundingRule]):
        increment_rule (Union[Unset, IncrementRule]):
        requires_london_allowance (Union[Unset, bool]): Requires LA column to be completed on the spine
        grade_effective_date (Union[Unset, datetime.date]): Effective date for applicable grades
        point_effective_date (Union[Unset, datetime.date]): Effective date for applicable spinal points
    """

    name: Union[Unset, None, str] = UNSET
    full_time_hours: Union[Unset, float] = UNSET
    full_time_weeks: Union[Unset, float] = UNSET
    salary_formula: Union[Unset, None, str] = UNSET
    hourly_divisor: Union[Unset, float] = UNSET
    hourly_decimals: Union[Unset, int] = UNSET
    daily_divisor: Union[Unset, float] = UNSET
    daily_decimals: Union[Unset, int] = UNSET
    annual_decimals: Union[Unset, int] = UNSET
    annual_rounding_rule: Union[Unset, AnnualRoundingRule] = UNSET
    increment_rule: Union[Unset, IncrementRule] = UNSET
    requires_london_allowance: Union[Unset, bool] = UNSET
    grade_effective_date: Union[Unset, datetime.date] = UNSET
    point_effective_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        full_time_hours = self.full_time_hours
        full_time_weeks = self.full_time_weeks
        salary_formula = self.salary_formula
        hourly_divisor = self.hourly_divisor
        hourly_decimals = self.hourly_decimals
        daily_divisor = self.daily_divisor
        daily_decimals = self.daily_decimals
        annual_decimals = self.annual_decimals
        annual_rounding_rule: Union[Unset, str] = UNSET
        if not isinstance(self.annual_rounding_rule, Unset):
            annual_rounding_rule = self.annual_rounding_rule.value

        increment_rule: Union[Unset, str] = UNSET
        if not isinstance(self.increment_rule, Unset):
            increment_rule = self.increment_rule.value

        requires_london_allowance = self.requires_london_allowance
        grade_effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.grade_effective_date, Unset):
            grade_effective_date = self.grade_effective_date.isoformat()

        point_effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.point_effective_date, Unset):
            point_effective_date = self.point_effective_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if full_time_hours is not UNSET:
            field_dict["fullTimeHours"] = full_time_hours
        if full_time_weeks is not UNSET:
            field_dict["fullTimeWeeks"] = full_time_weeks
        if salary_formula is not UNSET:
            field_dict["salaryFormula"] = salary_formula
        if hourly_divisor is not UNSET:
            field_dict["hourlyDivisor"] = hourly_divisor
        if hourly_decimals is not UNSET:
            field_dict["hourlyDecimals"] = hourly_decimals
        if daily_divisor is not UNSET:
            field_dict["dailyDivisor"] = daily_divisor
        if daily_decimals is not UNSET:
            field_dict["dailyDecimals"] = daily_decimals
        if annual_decimals is not UNSET:
            field_dict["annualDecimals"] = annual_decimals
        if annual_rounding_rule is not UNSET:
            field_dict["annualRoundingRule"] = annual_rounding_rule
        if increment_rule is not UNSET:
            field_dict["incrementRule"] = increment_rule
        if requires_london_allowance is not UNSET:
            field_dict["requiresLondonAllowance"] = requires_london_allowance
        if grade_effective_date is not UNSET:
            field_dict["gradeEffectiveDate"] = grade_effective_date
        if point_effective_date is not UNSET:
            field_dict["pointEffectiveDate"] = point_effective_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        full_time_hours = d.pop("fullTimeHours", UNSET)

        full_time_weeks = d.pop("fullTimeWeeks", UNSET)

        salary_formula = d.pop("salaryFormula", UNSET)

        hourly_divisor = d.pop("hourlyDivisor", UNSET)

        hourly_decimals = d.pop("hourlyDecimals", UNSET)

        daily_divisor = d.pop("dailyDivisor", UNSET)

        daily_decimals = d.pop("dailyDecimals", UNSET)

        annual_decimals = d.pop("annualDecimals", UNSET)

        _annual_rounding_rule = d.pop("annualRoundingRule", UNSET)
        annual_rounding_rule: Union[Unset, AnnualRoundingRule]
        if isinstance(_annual_rounding_rule,  Unset):
            annual_rounding_rule = UNSET
        else:
            annual_rounding_rule = AnnualRoundingRule(_annual_rounding_rule)




        _increment_rule = d.pop("incrementRule", UNSET)
        increment_rule: Union[Unset, IncrementRule]
        if isinstance(_increment_rule,  Unset):
            increment_rule = UNSET
        else:
            increment_rule = IncrementRule(_increment_rule)




        requires_london_allowance = d.pop("requiresLondonAllowance", UNSET)

        _grade_effective_date = d.pop("gradeEffectiveDate", UNSET)
        grade_effective_date: Union[Unset, datetime.date]
        if isinstance(_grade_effective_date,  Unset):
            grade_effective_date = UNSET
        else:
            grade_effective_date = isoparse(_grade_effective_date).date()




        _point_effective_date = d.pop("pointEffectiveDate", UNSET)
        point_effective_date: Union[Unset, datetime.date]
        if isinstance(_point_effective_date,  Unset):
            point_effective_date = UNSET
        else:
            point_effective_date = isoparse(_point_effective_date).date()




        contract_pay_spine_request = cls(
            name=name,
            full_time_hours=full_time_hours,
            full_time_weeks=full_time_weeks,
            salary_formula=salary_formula,
            hourly_divisor=hourly_divisor,
            hourly_decimals=hourly_decimals,
            daily_divisor=daily_divisor,
            daily_decimals=daily_decimals,
            annual_decimals=annual_decimals,
            annual_rounding_rule=annual_rounding_rule,
            increment_rule=increment_rule,
            requires_london_allowance=requires_london_allowance,
            grade_effective_date=grade_effective_date,
            point_effective_date=point_effective_date,
        )

        return contract_pay_spine_request

