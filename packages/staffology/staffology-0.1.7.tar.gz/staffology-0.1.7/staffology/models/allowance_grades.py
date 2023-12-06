import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllowanceGrades")

@attr.s(auto_attribs=True)
class AllowanceGrades:
    """
    Attributes:
        pay_spine_id (int):
        allowance_id (int):
        allowance_grade_payslip_text (Union[Unset, None, str]):
        allowance_grade_annual_value (Union[Unset, float]):
        allowance_grade_effective_date (Union[Unset, datetime.date]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    pay_spine_id: int
    allowance_id: int
    allowance_grade_payslip_text: Union[Unset, None, str] = UNSET
    allowance_grade_annual_value: Union[Unset, float] = UNSET
    allowance_grade_effective_date: Union[Unset, datetime.date] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pay_spine_id = self.pay_spine_id
        allowance_id = self.allowance_id
        allowance_grade_payslip_text = self.allowance_grade_payslip_text
        allowance_grade_annual_value = self.allowance_grade_annual_value
        allowance_grade_effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_grade_effective_date, Unset):
            allowance_grade_effective_date = self.allowance_grade_effective_date.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "paySpineId": pay_spine_id,
            "allowanceId": allowance_id,
        })
        if allowance_grade_payslip_text is not UNSET:
            field_dict["allowanceGradePayslipText"] = allowance_grade_payslip_text
        if allowance_grade_annual_value is not UNSET:
            field_dict["allowanceGradeAnnualValue"] = allowance_grade_annual_value
        if allowance_grade_effective_date is not UNSET:
            field_dict["allowanceGradeEffectiveDate"] = allowance_grade_effective_date
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_spine_id = d.pop("paySpineId")

        allowance_id = d.pop("allowanceId")

        allowance_grade_payslip_text = d.pop("allowanceGradePayslipText", UNSET)

        allowance_grade_annual_value = d.pop("allowanceGradeAnnualValue", UNSET)

        _allowance_grade_effective_date = d.pop("allowanceGradeEffectiveDate", UNSET)
        allowance_grade_effective_date: Union[Unset, datetime.date]
        if isinstance(_allowance_grade_effective_date,  Unset):
            allowance_grade_effective_date = UNSET
        else:
            allowance_grade_effective_date = isoparse(_allowance_grade_effective_date).date()




        id = d.pop("id", UNSET)

        allowance_grades = cls(
            pay_spine_id=pay_spine_id,
            allowance_id=allowance_id,
            allowance_grade_payslip_text=allowance_grade_payslip_text,
            allowance_grade_annual_value=allowance_grade_annual_value,
            allowance_grade_effective_date=allowance_grade_effective_date,
            id=id,
        )

        return allowance_grades

