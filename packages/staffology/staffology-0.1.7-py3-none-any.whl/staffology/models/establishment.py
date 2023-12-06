from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Establishment")

@attr.s(auto_attribs=True)
class Establishment:
    """
    Attributes:
        local_authority_number (Union[Unset, None, str]):
        school_employer_type (Union[Unset, None, str]):
        establishment_code (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    local_authority_number: Union[Unset, None, str] = UNSET
    school_employer_type: Union[Unset, None, str] = UNSET
    establishment_code: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        local_authority_number = self.local_authority_number
        school_employer_type = self.school_employer_type
        establishment_code = self.establishment_code
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if local_authority_number is not UNSET:
            field_dict["localAuthorityNumber"] = local_authority_number
        if school_employer_type is not UNSET:
            field_dict["schoolEmployerType"] = school_employer_type
        if establishment_code is not UNSET:
            field_dict["establishmentCode"] = establishment_code
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_authority_number = d.pop("localAuthorityNumber", UNSET)

        school_employer_type = d.pop("schoolEmployerType", UNSET)

        establishment_code = d.pop("establishmentCode", UNSET)

        id = d.pop("id", UNSET)

        establishment = cls(
            local_authority_number=local_authority_number,
            school_employer_type=school_employer_type,
            establishment_code=establishment_code,
            id=id,
        )

        return establishment

