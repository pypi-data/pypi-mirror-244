from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.bank_details import BankDetails
from ..models.day_of_week import DayOfWeek
from ..models.payment_date_rule import PaymentDateRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="Payee")

@attr.s(auto_attribs=True)
class Payee:
    """
    Attributes:
        title (str): The name of this Payee
        bank_details (Union[Unset, BankDetails]):
        payment_date_rule (Union[Unset, PaymentDateRule]):
        payment_date_day_of_week (Union[Unset, DayOfWeek]):
        payment_date_day_of_month (Union[Unset, None, int]):
        has_minimum_bank_details (Union[Unset, bool]): Denotes whether the payee has the minimum bank details to receive
            a payment
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: str
    bank_details: Union[Unset, BankDetails] = UNSET
    payment_date_rule: Union[Unset, PaymentDateRule] = UNSET
    payment_date_day_of_week: Union[Unset, DayOfWeek] = UNSET
    payment_date_day_of_month: Union[Unset, None, int] = UNSET
    has_minimum_bank_details: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        payment_date_rule: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date_rule, Unset):
            payment_date_rule = self.payment_date_rule.value

        payment_date_day_of_week: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date_day_of_week, Unset):
            payment_date_day_of_week = self.payment_date_day_of_week.value

        payment_date_day_of_month = self.payment_date_day_of_month
        has_minimum_bank_details = self.has_minimum_bank_details
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "title": title,
        })
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if payment_date_rule is not UNSET:
            field_dict["paymentDateRule"] = payment_date_rule
        if payment_date_day_of_week is not UNSET:
            field_dict["paymentDateDayOfWeek"] = payment_date_day_of_week
        if payment_date_day_of_month is not UNSET:
            field_dict["paymentDateDayOfMonth"] = payment_date_day_of_month
        if has_minimum_bank_details is not UNSET:
            field_dict["hasMinimumBankDetails"] = has_minimum_bank_details
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details,  Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)




        _payment_date_rule = d.pop("paymentDateRule", UNSET)
        payment_date_rule: Union[Unset, PaymentDateRule]
        if isinstance(_payment_date_rule,  Unset):
            payment_date_rule = UNSET
        else:
            payment_date_rule = PaymentDateRule(_payment_date_rule)




        _payment_date_day_of_week = d.pop("paymentDateDayOfWeek", UNSET)
        payment_date_day_of_week: Union[Unset, DayOfWeek]
        if isinstance(_payment_date_day_of_week,  Unset):
            payment_date_day_of_week = UNSET
        else:
            payment_date_day_of_week = DayOfWeek(_payment_date_day_of_week)




        payment_date_day_of_month = d.pop("paymentDateDayOfMonth", UNSET)

        has_minimum_bank_details = d.pop("hasMinimumBankDetails", UNSET)

        id = d.pop("id", UNSET)

        payee = cls(
            title=title,
            bank_details=bank_details,
            payment_date_rule=payment_date_rule,
            payment_date_day_of_week=payment_date_day_of_week,
            payment_date_day_of_month=payment_date_day_of_month,
            has_minimum_bank_details=has_minimum_bank_details,
            id=id,
        )

        return payee

