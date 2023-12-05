import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractAeAssessmentRequest")

@attr.s(auto_attribs=True)
class ContractAeAssessmentRequest:
    """As part of AutoEnrolment we assess your Employees to see if they need to be auto-enroled in a Pension.
This model shows the result of an assessment.

    Attributes:
        assessment_date (Union[Unset, datetime.date]):
    """

    assessment_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        assessment_date: Union[Unset, str] = UNSET
        if not isinstance(self.assessment_date, Unset):
            assessment_date = self.assessment_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if assessment_date is not UNSET:
            field_dict["assessmentDate"] = assessment_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _assessment_date = d.pop("assessmentDate", UNSET)
        assessment_date: Union[Unset, datetime.date]
        if isinstance(_assessment_date,  Unset):
            assessment_date = UNSET
        else:
            assessment_date = isoparse(_assessment_date).date()




        contract_ae_assessment_request = cls(
            assessment_date=assessment_date,
        )

        return contract_ae_assessment_request

