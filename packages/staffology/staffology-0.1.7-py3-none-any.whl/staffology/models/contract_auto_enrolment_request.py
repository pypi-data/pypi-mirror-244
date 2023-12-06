from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.ae_exclusion_code import AeExclusionCode
from ..models.ae_uk_worker import AeUKWorker
from ..models.contract_ae_assessment_request import ContractAeAssessmentRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractAutoEnrolmentRequest")

@attr.s(auto_attribs=True)
class ContractAutoEnrolmentRequest:
    """
    Attributes:
        last_assessment (Union[Unset, ContractAeAssessmentRequest]): As part of AutoEnrolment we assess your Employees
            to see if they need to be auto-enroled in a Pension.
            This model shows the result of an assessment.
        uk_worker (Union[Unset, AeUKWorker]):
        days_to_defer_assessment (Union[Unset, int]): The number of days, if any, to defer assessment of this employee.
            You're allowed to defer assessment of new employees by up to 3 months.
        defer_by_months_not_days (Union[Unset, bool]): If set to true then the value in DaysToDeferAssessment will be
            treated as a number of months, not a number of days
        exempt (Union[Unset, bool]):
        ae_exclusion_code (Union[Unset, AeExclusionCode]):
        ae_postponement_letter_sent (Union[Unset, bool]):
    """

    last_assessment: Union[Unset, ContractAeAssessmentRequest] = UNSET
    uk_worker: Union[Unset, AeUKWorker] = UNSET
    days_to_defer_assessment: Union[Unset, int] = UNSET
    defer_by_months_not_days: Union[Unset, bool] = UNSET
    exempt: Union[Unset, bool] = UNSET
    ae_exclusion_code: Union[Unset, AeExclusionCode] = UNSET
    ae_postponement_letter_sent: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        last_assessment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_assessment, Unset):
            last_assessment = self.last_assessment.to_dict()

        uk_worker: Union[Unset, str] = UNSET
        if not isinstance(self.uk_worker, Unset):
            uk_worker = self.uk_worker.value

        days_to_defer_assessment = self.days_to_defer_assessment
        defer_by_months_not_days = self.defer_by_months_not_days
        exempt = self.exempt
        ae_exclusion_code: Union[Unset, str] = UNSET
        if not isinstance(self.ae_exclusion_code, Unset):
            ae_exclusion_code = self.ae_exclusion_code.value

        ae_postponement_letter_sent = self.ae_postponement_letter_sent

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if last_assessment is not UNSET:
            field_dict["lastAssessment"] = last_assessment
        if uk_worker is not UNSET:
            field_dict["ukWorker"] = uk_worker
        if days_to_defer_assessment is not UNSET:
            field_dict["daysToDeferAssessment"] = days_to_defer_assessment
        if defer_by_months_not_days is not UNSET:
            field_dict["deferByMonthsNotDays"] = defer_by_months_not_days
        if exempt is not UNSET:
            field_dict["exempt"] = exempt
        if ae_exclusion_code is not UNSET:
            field_dict["aeExclusionCode"] = ae_exclusion_code
        if ae_postponement_letter_sent is not UNSET:
            field_dict["aePostponementLetterSent"] = ae_postponement_letter_sent

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _last_assessment = d.pop("lastAssessment", UNSET)
        last_assessment: Union[Unset, ContractAeAssessmentRequest]
        if isinstance(_last_assessment,  Unset):
            last_assessment = UNSET
        else:
            last_assessment = ContractAeAssessmentRequest.from_dict(_last_assessment)




        _uk_worker = d.pop("ukWorker", UNSET)
        uk_worker: Union[Unset, AeUKWorker]
        if isinstance(_uk_worker,  Unset):
            uk_worker = UNSET
        else:
            uk_worker = AeUKWorker(_uk_worker)




        days_to_defer_assessment = d.pop("daysToDeferAssessment", UNSET)

        defer_by_months_not_days = d.pop("deferByMonthsNotDays", UNSET)

        exempt = d.pop("exempt", UNSET)

        _ae_exclusion_code = d.pop("aeExclusionCode", UNSET)
        ae_exclusion_code: Union[Unset, AeExclusionCode]
        if isinstance(_ae_exclusion_code,  Unset):
            ae_exclusion_code = UNSET
        else:
            ae_exclusion_code = AeExclusionCode(_ae_exclusion_code)




        ae_postponement_letter_sent = d.pop("aePostponementLetterSent", UNSET)

        contract_auto_enrolment_request = cls(
            last_assessment=last_assessment,
            uk_worker=uk_worker,
            days_to_defer_assessment=days_to_defer_assessment,
            defer_by_months_not_days=defer_by_months_not_days,
            exempt=exempt,
            ae_exclusion_code=ae_exclusion_code,
            ae_postponement_letter_sent=ae_postponement_letter_sent,
        )

        return contract_auto_enrolment_request

