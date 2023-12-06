from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.pay_run_state import PayRunState
from ..models.pay_run_state_change_reason import PayRunStateChangeReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunStateChange")

@attr.s(auto_attribs=True)
class PayRunStateChange:
    """
    Attributes:
        state (Union[Unset, PayRunState]):
        reason (Union[Unset, PayRunStateChangeReason]):
        reason_text (Union[Unset, None, str]): A free-form text field for a reason for the change of state.
        employee_unique_ids (Union[Unset, None, List[str]]): List of employee unique ids, whose PayRunEntries to be re-
            opened during a Payrun rollback operation.
            Will be used only during a transition to a rolled back pay run state
    """

    state: Union[Unset, PayRunState] = UNSET
    reason: Union[Unset, PayRunStateChangeReason] = UNSET
    reason_text: Union[Unset, None, str] = UNSET
    employee_unique_ids: Union[Unset, None, List[str]] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        reason_text = self.reason_text
        employee_unique_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.employee_unique_ids, Unset):
            if self.employee_unique_ids is None:
                employee_unique_ids = None
            else:
                employee_unique_ids = self.employee_unique_ids





        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if state is not UNSET:
            field_dict["state"] = state
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reason_text is not UNSET:
            field_dict["reasonText"] = reason_text
        if employee_unique_ids is not UNSET:
            field_dict["employeeUniqueIds"] = employee_unique_ids

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




        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, PayRunStateChangeReason]
        if isinstance(_reason,  Unset):
            reason = UNSET
        else:
            reason = PayRunStateChangeReason(_reason)




        reason_text = d.pop("reasonText", UNSET)

        employee_unique_ids = cast(List[str], d.pop("employeeUniqueIds", UNSET))


        pay_run_state_change = cls(
            state=state,
            reason=reason,
            reason_text=reason_text,
            employee_unique_ids=employee_unique_ids,
        )

        return pay_run_state_change

