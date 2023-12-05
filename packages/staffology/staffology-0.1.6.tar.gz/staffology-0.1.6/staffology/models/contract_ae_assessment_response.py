import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.ae_employee_state import AeEmployeeState
from ..models.ae_exclusion_code import AeExclusionCode
from ..models.ae_status import AeStatus
from ..models.ae_uk_worker import AeUKWorker
from ..models.contract_ae_assessment_action import ContractAeAssessmentAction
from ..models.contract_employee_item import ContractEmployeeItem
from ..models.pay_periods import PayPeriods
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractAeAssessmentResponse")

@attr.s(auto_attribs=True)
class ContractAeAssessmentResponse:
    """
    Attributes:
        id (Union[Unset, str]): The unique id of the object
        employee_state (Union[Unset, AeEmployeeState]):
        age (Union[Unset, int]): The age of the Employee at the time of the assessment
        uk_worker (Union[Unset, AeUKWorker]):
        pay_period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]): The PaySchedule ordinal for the Employee at the time of the assessment
        earnings_in_period (Union[Unset, float]):
        qualifying_earnings_in_period (Union[Unset, float]):
        ae_exclusion_code (Union[Unset, AeExclusionCode]):
        status (Union[Unset, AeStatus]):
        reason (Union[Unset, None, str]): The reason for determining the Status given.
        action (Union[Unset, ContractAeAssessmentAction]):
        employee (Union[Unset, ContractEmployeeItem]):
        assessment_date (Union[Unset, datetime.date]):
    """

    id: Union[Unset, str] = UNSET
    employee_state: Union[Unset, AeEmployeeState] = UNSET
    age: Union[Unset, int] = UNSET
    uk_worker: Union[Unset, AeUKWorker] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    earnings_in_period: Union[Unset, float] = UNSET
    qualifying_earnings_in_period: Union[Unset, float] = UNSET
    ae_exclusion_code: Union[Unset, AeExclusionCode] = UNSET
    status: Union[Unset, AeStatus] = UNSET
    reason: Union[Unset, None, str] = UNSET
    action: Union[Unset, ContractAeAssessmentAction] = UNSET
    employee: Union[Unset, ContractEmployeeItem] = UNSET
    assessment_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        employee_state: Union[Unset, str] = UNSET
        if not isinstance(self.employee_state, Unset):
            employee_state = self.employee_state.value

        age = self.age
        uk_worker: Union[Unset, str] = UNSET
        if not isinstance(self.uk_worker, Unset):
            uk_worker = self.uk_worker.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        earnings_in_period = self.earnings_in_period
        qualifying_earnings_in_period = self.qualifying_earnings_in_period
        ae_exclusion_code: Union[Unset, str] = UNSET
        if not isinstance(self.ae_exclusion_code, Unset):
            ae_exclusion_code = self.ae_exclusion_code.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reason = self.reason
        action: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.to_dict()

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        assessment_date: Union[Unset, str] = UNSET
        if not isinstance(self.assessment_date, Unset):
            assessment_date = self.assessment_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if employee_state is not UNSET:
            field_dict["employeeState"] = employee_state
        if age is not UNSET:
            field_dict["age"] = age
        if uk_worker is not UNSET:
            field_dict["ukWorker"] = uk_worker
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if earnings_in_period is not UNSET:
            field_dict["earningsInPeriod"] = earnings_in_period
        if qualifying_earnings_in_period is not UNSET:
            field_dict["qualifyingEarningsInPeriod"] = qualifying_earnings_in_period
        if ae_exclusion_code is not UNSET:
            field_dict["aeExclusionCode"] = ae_exclusion_code
        if status is not UNSET:
            field_dict["status"] = status
        if reason is not UNSET:
            field_dict["reason"] = reason
        if action is not UNSET:
            field_dict["action"] = action
        if employee is not UNSET:
            field_dict["employee"] = employee
        if assessment_date is not UNSET:
            field_dict["assessmentDate"] = assessment_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _employee_state = d.pop("employeeState", UNSET)
        employee_state: Union[Unset, AeEmployeeState]
        if isinstance(_employee_state,  Unset):
            employee_state = UNSET
        else:
            employee_state = AeEmployeeState(_employee_state)




        age = d.pop("age", UNSET)

        _uk_worker = d.pop("ukWorker", UNSET)
        uk_worker: Union[Unset, AeUKWorker]
        if isinstance(_uk_worker,  Unset):
            uk_worker = UNSET
        else:
            uk_worker = AeUKWorker(_uk_worker)




        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period,  Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)




        ordinal = d.pop("ordinal", UNSET)

        earnings_in_period = d.pop("earningsInPeriod", UNSET)

        qualifying_earnings_in_period = d.pop("qualifyingEarningsInPeriod", UNSET)

        _ae_exclusion_code = d.pop("aeExclusionCode", UNSET)
        ae_exclusion_code: Union[Unset, AeExclusionCode]
        if isinstance(_ae_exclusion_code,  Unset):
            ae_exclusion_code = UNSET
        else:
            ae_exclusion_code = AeExclusionCode(_ae_exclusion_code)




        _status = d.pop("status", UNSET)
        status: Union[Unset, AeStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = AeStatus(_status)




        reason = d.pop("reason", UNSET)

        _action = d.pop("action", UNSET)
        action: Union[Unset, ContractAeAssessmentAction]
        if isinstance(_action,  Unset):
            action = UNSET
        else:
            action = ContractAeAssessmentAction.from_dict(_action)




        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, ContractEmployeeItem]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = ContractEmployeeItem.from_dict(_employee)




        _assessment_date = d.pop("assessmentDate", UNSET)
        assessment_date: Union[Unset, datetime.date]
        if isinstance(_assessment_date,  Unset):
            assessment_date = UNSET
        else:
            assessment_date = isoparse(_assessment_date).date()




        contract_ae_assessment_response = cls(
            id=id,
            employee_state=employee_state,
            age=age,
            uk_worker=uk_worker,
            pay_period=pay_period,
            ordinal=ordinal,
            earnings_in_period=earnings_in_period,
            qualifying_earnings_in_period=qualifying_earnings_in_period,
            ae_exclusion_code=ae_exclusion_code,
            status=status,
            reason=reason,
            action=action,
            employee=employee,
            assessment_date=assessment_date,
        )

        return contract_ae_assessment_response

