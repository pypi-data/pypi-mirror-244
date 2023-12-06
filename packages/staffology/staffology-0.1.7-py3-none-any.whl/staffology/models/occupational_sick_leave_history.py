import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OccupationalSickLeaveHistory")

@attr.s(auto_attribs=True)
class OccupationalSickLeaveHistory:
    """
    Attributes:
        leave_date (datetime.date):
        pay_percent (float):
        service_band_from (int):
        service_band_to (int):
        payroll_code (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    leave_date: datetime.date
    pay_percent: float
    service_band_from: int
    service_band_to: int
    payroll_code: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        leave_date = self.leave_date.isoformat() 
        pay_percent = self.pay_percent
        service_band_from = self.service_band_from
        service_band_to = self.service_band_to
        payroll_code = self.payroll_code
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "leaveDate": leave_date,
            "payPercent": pay_percent,
            "serviceBandFrom": service_band_from,
            "serviceBandTo": service_band_to,
        })
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        leave_date = isoparse(d.pop("leaveDate")).date()




        pay_percent = d.pop("payPercent")

        service_band_from = d.pop("serviceBandFrom")

        service_band_to = d.pop("serviceBandTo")

        payroll_code = d.pop("payrollCode", UNSET)

        id = d.pop("id", UNSET)

        occupational_sick_leave_history = cls(
            leave_date=leave_date,
            pay_percent=pay_percent,
            service_band_from=service_band_from,
            service_band_to=service_band_to,
            payroll_code=payroll_code,
            id=id,
        )

        return occupational_sick_leave_history

