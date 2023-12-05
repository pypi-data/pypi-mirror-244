from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TeachersPensionEoyLineItem")

@attr.s(auto_attribs=True)
class TeachersPensionEoyLineItem:
    """
    Attributes:
        tier (Union[Unset, float]):
        percentage_rate (Union[Unset, float]):
        contributory_salary (Union[Unset, float]):
        teachers_contributions (Union[Unset, float]):
        employers_contributions (Union[Unset, float]):
    """

    tier: Union[Unset, float] = UNSET
    percentage_rate: Union[Unset, float] = UNSET
    contributory_salary: Union[Unset, float] = UNSET
    teachers_contributions: Union[Unset, float] = UNSET
    employers_contributions: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        tier = self.tier
        percentage_rate = self.percentage_rate
        contributory_salary = self.contributory_salary
        teachers_contributions = self.teachers_contributions
        employers_contributions = self.employers_contributions

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if tier is not UNSET:
            field_dict["tier"] = tier
        if percentage_rate is not UNSET:
            field_dict["percentageRate"] = percentage_rate
        if contributory_salary is not UNSET:
            field_dict["contributorySalary"] = contributory_salary
        if teachers_contributions is not UNSET:
            field_dict["teachersContributions"] = teachers_contributions
        if employers_contributions is not UNSET:
            field_dict["employersContributions"] = employers_contributions

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tier = d.pop("tier", UNSET)

        percentage_rate = d.pop("percentageRate", UNSET)

        contributory_salary = d.pop("contributorySalary", UNSET)

        teachers_contributions = d.pop("teachersContributions", UNSET)

        employers_contributions = d.pop("employersContributions", UNSET)

        teachers_pension_eoy_line_item = cls(
            tier=tier,
            percentage_rate=percentage_rate,
            contributory_salary=contributory_salary,
            teachers_contributions=teachers_contributions,
            employers_contributions=employers_contributions,
        )

        return teachers_pension_eoy_line_item

