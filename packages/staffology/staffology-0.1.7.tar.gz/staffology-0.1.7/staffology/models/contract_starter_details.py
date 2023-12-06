import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.contract_overseas_employer_details import ContractOverseasEmployerDetails
from ..models.contract_pensioner_payroll import ContractPensionerPayroll
from ..models.starter_declaration import StarterDeclaration
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractStarterDetails")

@attr.s(auto_attribs=True)
class ContractStarterDetails:
    """
    Attributes:
        start_date (datetime.date):
        starter_declaration (StarterDeclaration):
        overseas_employer_details (Union[Unset, ContractOverseasEmployerDetails]):
        pensioner_payroll (Union[Unset, ContractPensionerPayroll]):
    """

    start_date: datetime.date
    starter_declaration: StarterDeclaration
    overseas_employer_details: Union[Unset, ContractOverseasEmployerDetails] = UNSET
    pensioner_payroll: Union[Unset, ContractPensionerPayroll] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        start_date = self.start_date.isoformat() 
        starter_declaration = self.starter_declaration.value

        overseas_employer_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.overseas_employer_details, Unset):
            overseas_employer_details = self.overseas_employer_details.to_dict()

        pensioner_payroll: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pensioner_payroll, Unset):
            pensioner_payroll = self.pensioner_payroll.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "startDate": start_date,
            "starterDeclaration": starter_declaration,
        })
        if overseas_employer_details is not UNSET:
            field_dict["overseasEmployerDetails"] = overseas_employer_details
        if pensioner_payroll is not UNSET:
            field_dict["pensionerPayroll"] = pensioner_payroll

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_date = isoparse(d.pop("startDate")).date()




        starter_declaration = StarterDeclaration(d.pop("starterDeclaration"))




        _overseas_employer_details = d.pop("overseasEmployerDetails", UNSET)
        overseas_employer_details: Union[Unset, ContractOverseasEmployerDetails]
        if isinstance(_overseas_employer_details,  Unset):
            overseas_employer_details = UNSET
        else:
            overseas_employer_details = ContractOverseasEmployerDetails.from_dict(_overseas_employer_details)




        _pensioner_payroll = d.pop("pensionerPayroll", UNSET)
        pensioner_payroll: Union[Unset, ContractPensionerPayroll]
        if isinstance(_pensioner_payroll,  Unset):
            pensioner_payroll = UNSET
        else:
            pensioner_payroll = ContractPensionerPayroll.from_dict(_pensioner_payroll)




        contract_starter_details = cls(
            start_date=start_date,
            starter_declaration=starter_declaration,
            overseas_employer_details=overseas_employer_details,
            pensioner_payroll=pensioner_payroll,
        )

        return contract_starter_details

