import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerEvcOptInHistory")

@attr.s(auto_attribs=True)
class EmployerEvcOptInHistory:
    """
    Attributes:
        opt_in (Union[Unset, bool]):
        date (Union[Unset, datetime.date]):
        user_email (Union[Unset, None, str]):
    """

    opt_in: Union[Unset, bool] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    user_email: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        opt_in = self.opt_in
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        user_email = self.user_email

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if opt_in is not UNSET:
            field_dict["optIn"] = opt_in
        if date is not UNSET:
            field_dict["date"] = date
        if user_email is not UNSET:
            field_dict["userEmail"] = user_email

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        opt_in = d.pop("optIn", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date,  Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()




        user_email = d.pop("userEmail", UNSET)

        employer_evc_opt_in_history = cls(
            opt_in=opt_in,
            date=date,
            user_email=user_email,
        )

        return employer_evc_opt_in_history

