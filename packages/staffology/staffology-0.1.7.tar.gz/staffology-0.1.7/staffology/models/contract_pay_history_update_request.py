import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.contract_pay_period_types import ContractPayPeriodTypes
from ..models.contract_tax_year_types import ContractTaxYearTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPayHistoryUpdateRequest")

@attr.s(auto_attribs=True)
class ContractPayHistoryUpdateRequest:
    """
    Attributes:
        id (Union[Unset, str]): Average Holiday Pay History identifier
        employee_id (Union[Unset, str]): Employee unique Id
        employee_role_id (Union[Unset, str]): Employee role unique Id
        tax_year (Union[Unset, ContractTaxYearTypes]):
        pay_period (Union[Unset, ContractPayPeriodTypes]):
        period_number (Union[Unset, int]): Tax Week or Tax Month number this PayRunEntry relates to
        pay_amount (Union[Unset, float]): monetary amount for given period, if not provided then 0
        hours (Union[Unset, float]): decimal amount of hours worked, if not provided then 0
        is_statutory_pay_only (Union[Unset, bool]): optional boolean flag, if the period only had SXP present
        payment_date (Union[Unset, datetime.date]): The date payment was made for respective period
    """

    id: Union[Unset, str] = UNSET
    employee_id: Union[Unset, str] = UNSET
    employee_role_id: Union[Unset, str] = UNSET
    tax_year: Union[Unset, ContractTaxYearTypes] = UNSET
    pay_period: Union[Unset, ContractPayPeriodTypes] = UNSET
    period_number: Union[Unset, int] = UNSET
    pay_amount: Union[Unset, float] = UNSET
    hours: Union[Unset, float] = UNSET
    is_statutory_pay_only: Union[Unset, bool] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        employee_id = self.employee_id
        employee_role_id = self.employee_role_id
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        period_number = self.period_number
        pay_amount = self.pay_amount
        hours = self.hours
        is_statutory_pay_only = self.is_statutory_pay_only
        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if employee_role_id is not UNSET:
            field_dict["employeeRoleId"] = employee_role_id
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if period_number is not UNSET:
            field_dict["periodNumber"] = period_number
        if pay_amount is not UNSET:
            field_dict["payAmount"] = pay_amount
        if hours is not UNSET:
            field_dict["hours"] = hours
        if is_statutory_pay_only is not UNSET:
            field_dict["isStatutoryPayOnly"] = is_statutory_pay_only
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        employee_id = d.pop("employeeId", UNSET)

        employee_role_id = d.pop("employeeRoleId", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, ContractTaxYearTypes]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = ContractTaxYearTypes(_tax_year)




        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, ContractPayPeriodTypes]
        if isinstance(_pay_period,  Unset):
            pay_period = UNSET
        else:
            pay_period = ContractPayPeriodTypes(_pay_period)




        period_number = d.pop("periodNumber", UNSET)

        pay_amount = d.pop("payAmount", UNSET)

        hours = d.pop("hours", UNSET)

        is_statutory_pay_only = d.pop("isStatutoryPayOnly", UNSET)

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date,  Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()




        contract_pay_history_update_request = cls(
            id=id,
            employee_id=employee_id,
            employee_role_id=employee_role_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            pay_amount=pay_amount,
            hours=hours,
            is_statutory_pay_only=is_statutory_pay_only,
            payment_date=payment_date,
        )

        return contract_pay_history_update_request

