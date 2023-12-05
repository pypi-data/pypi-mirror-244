import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.pay_periods import PayPeriods
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractP11HistoryResponse")

@attr.s(auto_attribs=True)
class ContractP11HistoryResponse:
    """
    Attributes:
        id (Union[Unset, str]):
        tax_year (Union[Unset, TaxYear]):
        pay_period (Union[Unset, PayPeriods]):
        period_number (Union[Unset, int]):
        niable_pay (Union[Unset, float]):
        pay_date (Union[Unset, datetime.date]):
    """

    id: Union[Unset, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    period_number: Union[Unset, int] = UNSET
    niable_pay: Union[Unset, float] = UNSET
    pay_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        period_number = self.period_number
        niable_pay = self.niable_pay
        pay_date: Union[Unset, str] = UNSET
        if not isinstance(self.pay_date, Unset):
            pay_date = self.pay_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if period_number is not UNSET:
            field_dict["periodNumber"] = period_number
        if niable_pay is not UNSET:
            field_dict["niablePay"] = niable_pay
        if pay_date is not UNSET:
            field_dict["payDate"] = pay_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)




        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period,  Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)




        period_number = d.pop("periodNumber", UNSET)

        niable_pay = d.pop("niablePay", UNSET)

        _pay_date = d.pop("payDate", UNSET)
        pay_date: Union[Unset, datetime.date]
        if isinstance(_pay_date,  Unset):
            pay_date = UNSET
        else:
            pay_date = isoparse(_pay_date).date()




        contract_p11_history_response = cls(
            id=id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            niable_pay=niable_pay,
            pay_date=pay_date,
        )

        return contract_p11_history_response

