from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.papdis_employer import PapdisEmployer
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisPensionProvider")

@attr.s(auto_attribs=True)
class PapdisPensionProvider:
    """
    Attributes:
        pension_provider_id (Union[Unset, None, str]): [readonly] Taken from the papdisProviderId property of the
            PensionProvider
        employers (Union[Unset, None, List[PapdisEmployer]]):
        account_no (Union[Unset, None, str]): [readonly]
    """

    pension_provider_id: Union[Unset, None, str] = UNSET
    employers: Union[Unset, None, List[PapdisEmployer]] = UNSET
    account_no: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pension_provider_id = self.pension_provider_id
        employers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employers, Unset):
            if self.employers is None:
                employers = None
            else:
                employers = []
                for employers_item_data in self.employers:
                    employers_item = employers_item_data.to_dict()

                    employers.append(employers_item)




        account_no = self.account_no

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pension_provider_id is not UNSET:
            field_dict["pensionProviderId"] = pension_provider_id
        if employers is not UNSET:
            field_dict["employers"] = employers
        if account_no is not UNSET:
            field_dict["accountNo"] = account_no

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pension_provider_id = d.pop("pensionProviderId", UNSET)

        employers = []
        _employers = d.pop("employers", UNSET)
        for employers_item_data in (_employers or []):
            employers_item = PapdisEmployer.from_dict(employers_item_data)



            employers.append(employers_item)


        account_no = d.pop("accountNo", UNSET)

        papdis_pension_provider = cls(
            pension_provider_id=pension_provider_id,
            employers=employers,
            account_no=account_no,
        )

        return papdis_pension_provider

