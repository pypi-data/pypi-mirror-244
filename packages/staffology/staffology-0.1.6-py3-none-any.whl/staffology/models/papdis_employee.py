import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.employee_role_pay_item import EmployeeRolePayItem
from ..models.papdis_employee_assessment import PapdisEmployeeAssessment
from ..models.papdis_employee_contact import PapdisEmployeeContact
from ..models.papdis_employee_contribution import PapdisEmployeeContribution
from ..models.papdis_employee_exit import PapdisEmployeeExit
from ..models.papdis_employee_identity import PapdisEmployeeIdentity
from ..models.papdis_employee_name import PapdisEmployeeName
from ..models.papdis_employee_pay import PapdisEmployeePay
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployee")

@attr.s(auto_attribs=True)
class PapdisEmployee:
    """
    Attributes:
        id (Union[Unset, int]): [readonly]
        employee_id (Union[Unset, str]): [readonly]
        name (Union[Unset, PapdisEmployeeName]):
        identity (Union[Unset, PapdisEmployeeIdentity]):
        contact (Union[Unset, PapdisEmployeeContact]):
        pay (Union[Unset, PapdisEmployeePay]):
        assessment (Union[Unset, PapdisEmployeeAssessment]):
        contribution (Union[Unset, PapdisEmployeeContribution]):
        exit_ (Union[Unset, PapdisEmployeeExit]):
        payroll_code (Union[Unset, None, str]): [readonly]
        ae_state_date (Union[Unset, None, datetime.date]):
        leave_date (Union[Unset, None, datetime.date]):
        state_pension_age (Union[Unset, int]):
        contractual_joiner_indicator (Union[Unset, bool]):
        job_title (Union[Unset, None, str]):
        pension_member_reference (Union[Unset, None, str]):
        pension_unique_id (Union[Unset, None, str]):
        employee_role_pay_items (Union[Unset, None, List[EmployeeRolePayItem]]):
    """

    id: Union[Unset, int] = UNSET
    employee_id: Union[Unset, str] = UNSET
    name: Union[Unset, PapdisEmployeeName] = UNSET
    identity: Union[Unset, PapdisEmployeeIdentity] = UNSET
    contact: Union[Unset, PapdisEmployeeContact] = UNSET
    pay: Union[Unset, PapdisEmployeePay] = UNSET
    assessment: Union[Unset, PapdisEmployeeAssessment] = UNSET
    contribution: Union[Unset, PapdisEmployeeContribution] = UNSET
    exit_: Union[Unset, PapdisEmployeeExit] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    ae_state_date: Union[Unset, None, datetime.date] = UNSET
    leave_date: Union[Unset, None, datetime.date] = UNSET
    state_pension_age: Union[Unset, int] = UNSET
    contractual_joiner_indicator: Union[Unset, bool] = UNSET
    job_title: Union[Unset, None, str] = UNSET
    pension_member_reference: Union[Unset, None, str] = UNSET
    pension_unique_id: Union[Unset, None, str] = UNSET
    employee_role_pay_items: Union[Unset, None, List[EmployeeRolePayItem]] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        employee_id = self.employee_id
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        identity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.identity, Unset):
            identity = self.identity.to_dict()

        contact: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        pay: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay, Unset):
            pay = self.pay.to_dict()

        assessment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assessment, Unset):
            assessment = self.assessment.to_dict()

        contribution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contribution, Unset):
            contribution = self.contribution.to_dict()

        exit_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exit_, Unset):
            exit_ = self.exit_.to_dict()

        payroll_code = self.payroll_code
        ae_state_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.ae_state_date, Unset):
            ae_state_date = self.ae_state_date.isoformat() if self.ae_state_date else None

        leave_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.leave_date, Unset):
            leave_date = self.leave_date.isoformat() if self.leave_date else None

        state_pension_age = self.state_pension_age
        contractual_joiner_indicator = self.contractual_joiner_indicator
        job_title = self.job_title
        pension_member_reference = self.pension_member_reference
        pension_unique_id = self.pension_unique_id
        employee_role_pay_items: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employee_role_pay_items, Unset):
            if self.employee_role_pay_items is None:
                employee_role_pay_items = None
            else:
                employee_role_pay_items = []
                for employee_role_pay_items_item_data in self.employee_role_pay_items:
                    employee_role_pay_items_item = employee_role_pay_items_item_data.to_dict()

                    employee_role_pay_items.append(employee_role_pay_items_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if name is not UNSET:
            field_dict["name"] = name
        if identity is not UNSET:
            field_dict["identity"] = identity
        if contact is not UNSET:
            field_dict["contact"] = contact
        if pay is not UNSET:
            field_dict["pay"] = pay
        if assessment is not UNSET:
            field_dict["assessment"] = assessment
        if contribution is not UNSET:
            field_dict["contribution"] = contribution
        if exit_ is not UNSET:
            field_dict["exit"] = exit_
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if ae_state_date is not UNSET:
            field_dict["aeStateDate"] = ae_state_date
        if leave_date is not UNSET:
            field_dict["leaveDate"] = leave_date
        if state_pension_age is not UNSET:
            field_dict["statePensionAge"] = state_pension_age
        if contractual_joiner_indicator is not UNSET:
            field_dict["contractualJoinerIndicator"] = contractual_joiner_indicator
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if pension_member_reference is not UNSET:
            field_dict["pensionMemberReference"] = pension_member_reference
        if pension_unique_id is not UNSET:
            field_dict["pensionUniqueId"] = pension_unique_id
        if employee_role_pay_items is not UNSET:
            field_dict["employeeRolePayItems"] = employee_role_pay_items

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        employee_id = d.pop("employeeId", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, PapdisEmployeeName]
        if isinstance(_name,  Unset):
            name = UNSET
        else:
            name = PapdisEmployeeName.from_dict(_name)




        _identity = d.pop("identity", UNSET)
        identity: Union[Unset, PapdisEmployeeIdentity]
        if isinstance(_identity,  Unset):
            identity = UNSET
        else:
            identity = PapdisEmployeeIdentity.from_dict(_identity)




        _contact = d.pop("contact", UNSET)
        contact: Union[Unset, PapdisEmployeeContact]
        if isinstance(_contact,  Unset):
            contact = UNSET
        else:
            contact = PapdisEmployeeContact.from_dict(_contact)




        _pay = d.pop("pay", UNSET)
        pay: Union[Unset, PapdisEmployeePay]
        if isinstance(_pay,  Unset):
            pay = UNSET
        else:
            pay = PapdisEmployeePay.from_dict(_pay)




        _assessment = d.pop("assessment", UNSET)
        assessment: Union[Unset, PapdisEmployeeAssessment]
        if isinstance(_assessment,  Unset):
            assessment = UNSET
        else:
            assessment = PapdisEmployeeAssessment.from_dict(_assessment)




        _contribution = d.pop("contribution", UNSET)
        contribution: Union[Unset, PapdisEmployeeContribution]
        if isinstance(_contribution,  Unset):
            contribution = UNSET
        else:
            contribution = PapdisEmployeeContribution.from_dict(_contribution)




        _exit_ = d.pop("exit", UNSET)
        exit_: Union[Unset, PapdisEmployeeExit]
        if isinstance(_exit_,  Unset):
            exit_ = UNSET
        else:
            exit_ = PapdisEmployeeExit.from_dict(_exit_)




        payroll_code = d.pop("payrollCode", UNSET)

        _ae_state_date = d.pop("aeStateDate", UNSET)
        ae_state_date: Union[Unset, None, datetime.date]
        if _ae_state_date is None:
            ae_state_date = None
        elif isinstance(_ae_state_date,  Unset):
            ae_state_date = UNSET
        else:
            ae_state_date = isoparse(_ae_state_date).date()




        _leave_date = d.pop("leaveDate", UNSET)
        leave_date: Union[Unset, None, datetime.date]
        if _leave_date is None:
            leave_date = None
        elif isinstance(_leave_date,  Unset):
            leave_date = UNSET
        else:
            leave_date = isoparse(_leave_date).date()




        state_pension_age = d.pop("statePensionAge", UNSET)

        contractual_joiner_indicator = d.pop("contractualJoinerIndicator", UNSET)

        job_title = d.pop("jobTitle", UNSET)

        pension_member_reference = d.pop("pensionMemberReference", UNSET)

        pension_unique_id = d.pop("pensionUniqueId", UNSET)

        employee_role_pay_items = []
        _employee_role_pay_items = d.pop("employeeRolePayItems", UNSET)
        for employee_role_pay_items_item_data in (_employee_role_pay_items or []):
            employee_role_pay_items_item = EmployeeRolePayItem.from_dict(employee_role_pay_items_item_data)



            employee_role_pay_items.append(employee_role_pay_items_item)


        papdis_employee = cls(
            id=id,
            employee_id=employee_id,
            name=name,
            identity=identity,
            contact=contact,
            pay=pay,
            assessment=assessment,
            contribution=contribution,
            exit_=exit_,
            payroll_code=payroll_code,
            ae_state_date=ae_state_date,
            leave_date=leave_date,
            state_pension_age=state_pension_age,
            contractual_joiner_indicator=contractual_joiner_indicator,
            job_title=job_title,
            pension_member_reference=pension_member_reference,
            pension_unique_id=pension_unique_id,
            employee_role_pay_items=employee_role_pay_items,
        )

        return papdis_employee

