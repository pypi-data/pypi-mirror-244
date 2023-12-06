import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPensionerPayroll")

@attr.s(auto_attribs=True)
class ContractPensionerPayroll:
    """
    Attributes:
        in_receipt_of_pension (Union[Unset, bool]): If set to true then the FPS will have the OccPenInd flag set to
            'yes'
        bereaved (Union[Unset, bool]): Indicator that Occupational Pension is being paid because they are a recently
            bereaved Spouse/Civil Partner
        amount (Union[Unset, float]): Annual amount of occupational pension
        start_date (Union[Unset, None, datetime.date]): Start date of occupational Pension
    """

    in_receipt_of_pension: Union[Unset, bool] = UNSET
    bereaved: Union[Unset, bool] = UNSET
    amount: Union[Unset, float] = UNSET
    start_date: Union[Unset, None, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        in_receipt_of_pension = self.in_receipt_of_pension
        bereaved = self.bereaved
        amount = self.amount
        start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat() if self.start_date else None


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if in_receipt_of_pension is not UNSET:
            field_dict["inReceiptOfPension"] = in_receipt_of_pension
        if bereaved is not UNSET:
            field_dict["bereaved"] = bereaved
        if amount is not UNSET:
            field_dict["amount"] = amount
        if start_date is not UNSET:
            field_dict["startDate"] = start_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        in_receipt_of_pension = d.pop("inReceiptOfPension", UNSET)

        bereaved = d.pop("bereaved", UNSET)

        amount = d.pop("amount", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, None, datetime.date]
        if _start_date is None:
            start_date = None
        elif isinstance(_start_date,  Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()




        contract_pensioner_payroll = cls(
            in_receipt_of_pension=in_receipt_of_pension,
            bereaved=bereaved,
            amount=amount,
            start_date=start_date,
        )

        return contract_pensioner_payroll

