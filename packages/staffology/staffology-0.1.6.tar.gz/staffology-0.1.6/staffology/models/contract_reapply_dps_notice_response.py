from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractReapplyDpsNoticeResponse")

@attr.s(auto_attribs=True)
class ContractReapplyDpsNoticeResponse:
    """
    Attributes:
        number_of_applied_notices (Union[Unset, int]):
        number_of_failed_notices (Union[Unset, int]):
    """

    number_of_applied_notices: Union[Unset, int] = UNSET
    number_of_failed_notices: Union[Unset, int] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        number_of_applied_notices = self.number_of_applied_notices
        number_of_failed_notices = self.number_of_failed_notices

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if number_of_applied_notices is not UNSET:
            field_dict["numberOfAppliedNotices"] = number_of_applied_notices
        if number_of_failed_notices is not UNSET:
            field_dict["numberOfFailedNotices"] = number_of_failed_notices

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        number_of_applied_notices = d.pop("numberOfAppliedNotices", UNSET)

        number_of_failed_notices = d.pop("numberOfFailedNotices", UNSET)

        contract_reapply_dps_notice_response = cls(
            number_of_applied_notices=number_of_applied_notices,
            number_of_failed_notices=number_of_failed_notices,
        )

        return contract_reapply_dps_notice_response

