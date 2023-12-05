import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.contract_auto_enrolment_request import ContractAutoEnrolmentRequest
from ..models.contract_bank_details import ContractBankDetails
from ..models.contract_employment_details_request import ContractEmploymentDetailsRequest
from ..models.contract_leave_settings_request import ContractLeaveSettingsRequest
from ..models.contract_pay_options_request import ContractPayOptionsRequest
from ..models.contract_personal_details_request import ContractPersonalDetailsRequest
from ..models.contract_right_to_work import ContractRightToWork
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractCreateEmployeeRequest")

@attr.s(auto_attribs=True)
class ContractCreateEmployeeRequest:
    """
    Attributes:
        personal_details (Union[Unset, ContractPersonalDetailsRequest]):
        employment_details (Union[Unset, ContractEmploymentDetailsRequest]):
        auto_enrolment (Union[Unset, ContractAutoEnrolmentRequest]):
        leave_settings (Union[Unset, ContractLeaveSettingsRequest]):
        right_to_work (Union[Unset, ContractRightToWork]):
        bank_details (Union[Unset, ContractBankDetails]):
        pay_options (Union[Unset, ContractPayOptionsRequest]):
        tags (Union[Unset, None, List[str]]):
        holiday_scheme_unique_id (Union[Unset, None, str]):
        aggregated_service_date (Union[Unset, None, datetime.date]):
        evc_id (Union[Unset, None, str]): If set then this will be used as the EmployeeIDFromProduct sent to EVC in
            place of the standard EmployeeId.
        source_system_id (Union[Unset, None, str]): Used by external systems so they can store an immutable reference.
            Once this property is set it cannot be changed.
    """

    personal_details: Union[Unset, ContractPersonalDetailsRequest] = UNSET
    employment_details: Union[Unset, ContractEmploymentDetailsRequest] = UNSET
    auto_enrolment: Union[Unset, ContractAutoEnrolmentRequest] = UNSET
    leave_settings: Union[Unset, ContractLeaveSettingsRequest] = UNSET
    right_to_work: Union[Unset, ContractRightToWork] = UNSET
    bank_details: Union[Unset, ContractBankDetails] = UNSET
    pay_options: Union[Unset, ContractPayOptionsRequest] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    holiday_scheme_unique_id: Union[Unset, None, str] = UNSET
    aggregated_service_date: Union[Unset, None, datetime.date] = UNSET
    evc_id: Union[Unset, None, str] = UNSET
    source_system_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        personal_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.personal_details, Unset):
            personal_details = self.personal_details.to_dict()

        employment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employment_details, Unset):
            employment_details = self.employment_details.to_dict()

        auto_enrolment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_enrolment, Unset):
            auto_enrolment = self.auto_enrolment.to_dict()

        leave_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leave_settings, Unset):
            leave_settings = self.leave_settings.to_dict()

        right_to_work: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.right_to_work, Unset):
            right_to_work = self.right_to_work.to_dict()

        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags




        holiday_scheme_unique_id = self.holiday_scheme_unique_id
        aggregated_service_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.aggregated_service_date, Unset):
            aggregated_service_date = self.aggregated_service_date.isoformat() if self.aggregated_service_date else None

        evc_id = self.evc_id
        source_system_id = self.source_system_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if personal_details is not UNSET:
            field_dict["personalDetails"] = personal_details
        if employment_details is not UNSET:
            field_dict["employmentDetails"] = employment_details
        if auto_enrolment is not UNSET:
            field_dict["autoEnrolment"] = auto_enrolment
        if leave_settings is not UNSET:
            field_dict["leaveSettings"] = leave_settings
        if right_to_work is not UNSET:
            field_dict["rightToWork"] = right_to_work
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options
        if tags is not UNSET:
            field_dict["tags"] = tags
        if holiday_scheme_unique_id is not UNSET:
            field_dict["holidaySchemeUniqueId"] = holiday_scheme_unique_id
        if aggregated_service_date is not UNSET:
            field_dict["aggregatedServiceDate"] = aggregated_service_date
        if evc_id is not UNSET:
            field_dict["evcId"] = evc_id
        if source_system_id is not UNSET:
            field_dict["sourceSystemId"] = source_system_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _personal_details = d.pop("personalDetails", UNSET)
        personal_details: Union[Unset, ContractPersonalDetailsRequest]
        if isinstance(_personal_details,  Unset):
            personal_details = UNSET
        else:
            personal_details = ContractPersonalDetailsRequest.from_dict(_personal_details)




        _employment_details = d.pop("employmentDetails", UNSET)
        employment_details: Union[Unset, ContractEmploymentDetailsRequest]
        if isinstance(_employment_details,  Unset):
            employment_details = UNSET
        else:
            employment_details = ContractEmploymentDetailsRequest.from_dict(_employment_details)




        _auto_enrolment = d.pop("autoEnrolment", UNSET)
        auto_enrolment: Union[Unset, ContractAutoEnrolmentRequest]
        if isinstance(_auto_enrolment,  Unset):
            auto_enrolment = UNSET
        else:
            auto_enrolment = ContractAutoEnrolmentRequest.from_dict(_auto_enrolment)




        _leave_settings = d.pop("leaveSettings", UNSET)
        leave_settings: Union[Unset, ContractLeaveSettingsRequest]
        if isinstance(_leave_settings,  Unset):
            leave_settings = UNSET
        else:
            leave_settings = ContractLeaveSettingsRequest.from_dict(_leave_settings)




        _right_to_work = d.pop("rightToWork", UNSET)
        right_to_work: Union[Unset, ContractRightToWork]
        if isinstance(_right_to_work,  Unset):
            right_to_work = UNSET
        else:
            right_to_work = ContractRightToWork.from_dict(_right_to_work)




        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, ContractBankDetails]
        if isinstance(_bank_details,  Unset):
            bank_details = UNSET
        else:
            bank_details = ContractBankDetails.from_dict(_bank_details)




        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, ContractPayOptionsRequest]
        if isinstance(_pay_options,  Unset):
            pay_options = UNSET
        else:
            pay_options = ContractPayOptionsRequest.from_dict(_pay_options)




        tags = cast(List[str], d.pop("tags", UNSET))


        holiday_scheme_unique_id = d.pop("holidaySchemeUniqueId", UNSET)

        _aggregated_service_date = d.pop("aggregatedServiceDate", UNSET)
        aggregated_service_date: Union[Unset, None, datetime.date]
        if _aggregated_service_date is None:
            aggregated_service_date = None
        elif isinstance(_aggregated_service_date,  Unset):
            aggregated_service_date = UNSET
        else:
            aggregated_service_date = isoparse(_aggregated_service_date).date()




        evc_id = d.pop("evcId", UNSET)

        source_system_id = d.pop("sourceSystemId", UNSET)

        contract_create_employee_request = cls(
            personal_details=personal_details,
            employment_details=employment_details,
            auto_enrolment=auto_enrolment,
            leave_settings=leave_settings,
            right_to_work=right_to_work,
            bank_details=bank_details,
            pay_options=pay_options,
            tags=tags,
            holiday_scheme_unique_id=holiday_scheme_unique_id,
            aggregated_service_date=aggregated_service_date,
            evc_id=evc_id,
            source_system_id=source_system_id,
        )

        return contract_create_employee_request

