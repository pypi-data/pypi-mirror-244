import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.contract_auto_enrolment_response import ContractAutoEnrolmentResponse
from ..models.contract_bank_details import ContractBankDetails
from ..models.contract_employment_details_response import ContractEmploymentDetailsResponse
from ..models.contract_leave_settings_response import ContractLeaveSettingsResponse
from ..models.contract_pay_options_response import ContractPayOptionsResponse
from ..models.contract_personal_details_response import ContractPersonalDetailsResponse
from ..models.contract_right_to_work import ContractRightToWork
from ..models.employee_status import EmployeeStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractEmployeeResponse")

@attr.s(auto_attribs=True)
class ContractEmployeeResponse:
    """
    Attributes:
        id (Union[Unset, str]): The unique id of the object
        personal_details (Union[Unset, ContractPersonalDetailsResponse]):
        employment_details (Union[Unset, ContractEmploymentDetailsResponse]):
        auto_enrolment (Union[Unset, ContractAutoEnrolmentResponse]):
        leave_settings (Union[Unset, ContractLeaveSettingsResponse]):
        right_to_work (Union[Unset, ContractRightToWork]):
        bank_details (Union[Unset, ContractBankDetails]):
        pay_options (Union[Unset, ContractPayOptionsResponse]):
        tags (Union[Unset, None, List[str]]):
        status (Union[Unset, EmployeeStatus]):
        ae_not_enroled_warning (Union[Unset, bool]):
        source_system_id (Union[Unset, None, str]):
        aggregated_service_date (Union[Unset, None, datetime.date]):
        holiday_scheme_unique_id (Union[Unset, None, str]):
        evc_id (Union[Unset, None, str]): If set then this will be used as the EmployeeIDFromProduct sent to EVC in
            place of the standard EmployeeId.
    """

    id: Union[Unset, str] = UNSET
    personal_details: Union[Unset, ContractPersonalDetailsResponse] = UNSET
    employment_details: Union[Unset, ContractEmploymentDetailsResponse] = UNSET
    auto_enrolment: Union[Unset, ContractAutoEnrolmentResponse] = UNSET
    leave_settings: Union[Unset, ContractLeaveSettingsResponse] = UNSET
    right_to_work: Union[Unset, ContractRightToWork] = UNSET
    bank_details: Union[Unset, ContractBankDetails] = UNSET
    pay_options: Union[Unset, ContractPayOptionsResponse] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    status: Union[Unset, EmployeeStatus] = UNSET
    ae_not_enroled_warning: Union[Unset, bool] = UNSET
    source_system_id: Union[Unset, None, str] = UNSET
    aggregated_service_date: Union[Unset, None, datetime.date] = UNSET
    holiday_scheme_unique_id: Union[Unset, None, str] = UNSET
    evc_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
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




        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        ae_not_enroled_warning = self.ae_not_enroled_warning
        source_system_id = self.source_system_id
        aggregated_service_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.aggregated_service_date, Unset):
            aggregated_service_date = self.aggregated_service_date.isoformat() if self.aggregated_service_date else None

        holiday_scheme_unique_id = self.holiday_scheme_unique_id
        evc_id = self.evc_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
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
        if status is not UNSET:
            field_dict["status"] = status
        if ae_not_enroled_warning is not UNSET:
            field_dict["aeNotEnroledWarning"] = ae_not_enroled_warning
        if source_system_id is not UNSET:
            field_dict["sourceSystemId"] = source_system_id
        if aggregated_service_date is not UNSET:
            field_dict["aggregatedServiceDate"] = aggregated_service_date
        if holiday_scheme_unique_id is not UNSET:
            field_dict["holidaySchemeUniqueId"] = holiday_scheme_unique_id
        if evc_id is not UNSET:
            field_dict["evcId"] = evc_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _personal_details = d.pop("personalDetails", UNSET)
        personal_details: Union[Unset, ContractPersonalDetailsResponse]
        if isinstance(_personal_details,  Unset):
            personal_details = UNSET
        else:
            personal_details = ContractPersonalDetailsResponse.from_dict(_personal_details)




        _employment_details = d.pop("employmentDetails", UNSET)
        employment_details: Union[Unset, ContractEmploymentDetailsResponse]
        if isinstance(_employment_details,  Unset):
            employment_details = UNSET
        else:
            employment_details = ContractEmploymentDetailsResponse.from_dict(_employment_details)




        _auto_enrolment = d.pop("autoEnrolment", UNSET)
        auto_enrolment: Union[Unset, ContractAutoEnrolmentResponse]
        if isinstance(_auto_enrolment,  Unset):
            auto_enrolment = UNSET
        else:
            auto_enrolment = ContractAutoEnrolmentResponse.from_dict(_auto_enrolment)




        _leave_settings = d.pop("leaveSettings", UNSET)
        leave_settings: Union[Unset, ContractLeaveSettingsResponse]
        if isinstance(_leave_settings,  Unset):
            leave_settings = UNSET
        else:
            leave_settings = ContractLeaveSettingsResponse.from_dict(_leave_settings)




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
        pay_options: Union[Unset, ContractPayOptionsResponse]
        if isinstance(_pay_options,  Unset):
            pay_options = UNSET
        else:
            pay_options = ContractPayOptionsResponse.from_dict(_pay_options)




        tags = cast(List[str], d.pop("tags", UNSET))


        _status = d.pop("status", UNSET)
        status: Union[Unset, EmployeeStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = EmployeeStatus(_status)




        ae_not_enroled_warning = d.pop("aeNotEnroledWarning", UNSET)

        source_system_id = d.pop("sourceSystemId", UNSET)

        _aggregated_service_date = d.pop("aggregatedServiceDate", UNSET)
        aggregated_service_date: Union[Unset, None, datetime.date]
        if _aggregated_service_date is None:
            aggregated_service_date = None
        elif isinstance(_aggregated_service_date,  Unset):
            aggregated_service_date = UNSET
        else:
            aggregated_service_date = isoparse(_aggregated_service_date).date()




        holiday_scheme_unique_id = d.pop("holidaySchemeUniqueId", UNSET)

        evc_id = d.pop("evcId", UNSET)

        contract_employee_response = cls(
            id=id,
            personal_details=personal_details,
            employment_details=employment_details,
            auto_enrolment=auto_enrolment,
            leave_settings=leave_settings,
            right_to_work=right_to_work,
            bank_details=bank_details,
            pay_options=pay_options,
            tags=tags,
            status=status,
            ae_not_enroled_warning=ae_not_enroled_warning,
            source_system_id=source_system_id,
            aggregated_service_date=aggregated_service_date,
            holiday_scheme_unique_id=holiday_scheme_unique_id,
            evc_id=evc_id,
        )

        return contract_employee_response

