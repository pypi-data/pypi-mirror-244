import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.pay_run_state import PayRunState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPayRunStateHistoryResponse")

@attr.s(auto_attribs=True)
class ContractPayRunStateHistoryResponse:
    """
    Attributes:
        state (Union[Unset, PayRunState]):
        created_date (Union[Unset, datetime.date]): Date in which the State was changed
    """

    state: Union[Unset, PayRunState] = UNSET
    created_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if state is not UNSET:
            field_dict["state"] = state
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, PayRunState]
        if isinstance(_state,  Unset):
            state = UNSET
        else:
            state = PayRunState(_state)




        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.date]
        if isinstance(_created_date,  Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date).date()




        contract_pay_run_state_history_response = cls(
            state=state,
            created_date=created_date,
        )

        return contract_pay_run_state_history_response

