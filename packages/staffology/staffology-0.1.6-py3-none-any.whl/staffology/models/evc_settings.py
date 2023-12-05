from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvcSettings")

@attr.s(auto_attribs=True)
class EvcSettings:
    """Employee Settings related to the Employee Verification Programme

    Attributes:
        right_to_restrict (Union[Unset, bool]): If set to True then this employee shouldn't be included in data sent to
            EVC
        right_to_delete (Union[Unset, bool]): If set to True then the EVC service will be informed that the employee has
            invoked their GDPR Right To Delete
        subject_access_request (Union[Unset, bool]): If set to True then the EVC service will be informed that the
            employee has made a Subject Access Request
        employee (Union[Unset, Item]):
    """

    right_to_restrict: Union[Unset, bool] = UNSET
    right_to_delete: Union[Unset, bool] = UNSET
    subject_access_request: Union[Unset, bool] = UNSET
    employee: Union[Unset, Item] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        right_to_restrict = self.right_to_restrict
        right_to_delete = self.right_to_delete
        subject_access_request = self.subject_access_request
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if right_to_restrict is not UNSET:
            field_dict["rightToRestrict"] = right_to_restrict
        if right_to_delete is not UNSET:
            field_dict["rightToDelete"] = right_to_delete
        if subject_access_request is not UNSET:
            field_dict["subjectAccessRequest"] = subject_access_request
        if employee is not UNSET:
            field_dict["employee"] = employee

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        right_to_restrict = d.pop("rightToRestrict", UNSET)

        right_to_delete = d.pop("rightToDelete", UNSET)

        subject_access_request = d.pop("subjectAccessRequest", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        evc_settings = cls(
            right_to_restrict=right_to_restrict,
            right_to_delete=right_to_delete,
            subject_access_request=subject_access_request,
            employee=employee,
        )

        return evc_settings

