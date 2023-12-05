from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cis_sub_contractor_type import CISSubContractorType
from ..models.contract_cis_verification_details_response import ContractCisVerificationDetailsResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractCisDetailsResponse")

@attr.s(auto_attribs=True)
class ContractCisDetailsResponse:
    """
    Attributes:
        verification (Union[Unset, ContractCisVerificationDetailsResponse]):
        type (Union[Unset, CISSubContractorType]):
        utr (Union[Unset, None, str]):
        trading_name (Union[Unset, None, str]):
        company_utr (Union[Unset, None, str]):
        company_number (Union[Unset, None, str]):
        vat_registered (Union[Unset, bool]):
        vat_number (Union[Unset, None, str]):
        vat_rate (Union[Unset, float]):
        reverse_charge_vat (Union[Unset, bool]):
    """

    verification: Union[Unset, ContractCisVerificationDetailsResponse] = UNSET
    type: Union[Unset, CISSubContractorType] = UNSET
    utr: Union[Unset, None, str] = UNSET
    trading_name: Union[Unset, None, str] = UNSET
    company_utr: Union[Unset, None, str] = UNSET
    company_number: Union[Unset, None, str] = UNSET
    vat_registered: Union[Unset, bool] = UNSET
    vat_number: Union[Unset, None, str] = UNSET
    vat_rate: Union[Unset, float] = UNSET
    reverse_charge_vat: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        verification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.verification, Unset):
            verification = self.verification.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        utr = self.utr
        trading_name = self.trading_name
        company_utr = self.company_utr
        company_number = self.company_number
        vat_registered = self.vat_registered
        vat_number = self.vat_number
        vat_rate = self.vat_rate
        reverse_charge_vat = self.reverse_charge_vat

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if verification is not UNSET:
            field_dict["verification"] = verification
        if type is not UNSET:
            field_dict["type"] = type
        if utr is not UNSET:
            field_dict["utr"] = utr
        if trading_name is not UNSET:
            field_dict["tradingName"] = trading_name
        if company_utr is not UNSET:
            field_dict["companyUtr"] = company_utr
        if company_number is not UNSET:
            field_dict["companyNumber"] = company_number
        if vat_registered is not UNSET:
            field_dict["vatRegistered"] = vat_registered
        if vat_number is not UNSET:
            field_dict["vatNumber"] = vat_number
        if vat_rate is not UNSET:
            field_dict["vatRate"] = vat_rate
        if reverse_charge_vat is not UNSET:
            field_dict["reverseChargeVAT"] = reverse_charge_vat

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _verification = d.pop("verification", UNSET)
        verification: Union[Unset, ContractCisVerificationDetailsResponse]
        if isinstance(_verification,  Unset):
            verification = UNSET
        else:
            verification = ContractCisVerificationDetailsResponse.from_dict(_verification)




        _type = d.pop("type", UNSET)
        type: Union[Unset, CISSubContractorType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = CISSubContractorType(_type)




        utr = d.pop("utr", UNSET)

        trading_name = d.pop("tradingName", UNSET)

        company_utr = d.pop("companyUtr", UNSET)

        company_number = d.pop("companyNumber", UNSET)

        vat_registered = d.pop("vatRegistered", UNSET)

        vat_number = d.pop("vatNumber", UNSET)

        vat_rate = d.pop("vatRate", UNSET)

        reverse_charge_vat = d.pop("reverseChargeVAT", UNSET)

        contract_cis_details_response = cls(
            verification=verification,
            type=type,
            utr=utr,
            trading_name=trading_name,
            company_utr=company_utr,
            company_number=company_number,
            vat_registered=vat_registered,
            vat_number=vat_number,
            vat_rate=vat_rate,
            reverse_charge_vat=reverse_charge_vat,
        )

        return contract_cis_details_response

