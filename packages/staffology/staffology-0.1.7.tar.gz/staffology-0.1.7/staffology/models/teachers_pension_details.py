from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.teachers_pension_employment_type import TeachersPensionEmploymentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TeachersPensionDetails")

@attr.s(auto_attribs=True)
class TeachersPensionDetails:
    """Used to represent additional information needed for
Teachers' Pensions

    Attributes:
        employment_type (Union[Unset, TeachersPensionEmploymentType]):
        full_time_salary (Union[Unset, None, int]): Up to 7 digits, in pounds. eg 24000
        part_time_salary_paid (Union[Unset, None, int]): Up to 7 digits, in pounds. eg 24000
        mcr_role_id_1 (Union[Unset, None, str]): Data field for the Contract used for Teachers pension administration
        mcr_role_id_2 (Union[Unset, None, str]): The Job role within the contract used for Teachers pension
            administration
        teachers_pension_admin_ni_number (Union[Unset, None, str]): Where an employee does not have an NI number yet (or
            doesn't know their NI number) Teachers Pensions will issue an administrative NI number
    """

    employment_type: Union[Unset, TeachersPensionEmploymentType] = UNSET
    full_time_salary: Union[Unset, None, int] = UNSET
    part_time_salary_paid: Union[Unset, None, int] = UNSET
    mcr_role_id_1: Union[Unset, None, str] = UNSET
    mcr_role_id_2: Union[Unset, None, str] = UNSET
    teachers_pension_admin_ni_number: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        employment_type: Union[Unset, str] = UNSET
        if not isinstance(self.employment_type, Unset):
            employment_type = self.employment_type.value

        full_time_salary = self.full_time_salary
        part_time_salary_paid = self.part_time_salary_paid
        mcr_role_id_1 = self.mcr_role_id_1
        mcr_role_id_2 = self.mcr_role_id_2
        teachers_pension_admin_ni_number = self.teachers_pension_admin_ni_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if employment_type is not UNSET:
            field_dict["employmentType"] = employment_type
        if full_time_salary is not UNSET:
            field_dict["fullTimeSalary"] = full_time_salary
        if part_time_salary_paid is not UNSET:
            field_dict["partTimeSalaryPaid"] = part_time_salary_paid
        if mcr_role_id_1 is not UNSET:
            field_dict["mcrRoleId1"] = mcr_role_id_1
        if mcr_role_id_2 is not UNSET:
            field_dict["mcrRoleId2"] = mcr_role_id_2
        if teachers_pension_admin_ni_number is not UNSET:
            field_dict["teachersPensionAdminNiNumber"] = teachers_pension_admin_ni_number

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employment_type = d.pop("employmentType", UNSET)
        employment_type: Union[Unset, TeachersPensionEmploymentType]
        if isinstance(_employment_type,  Unset):
            employment_type = UNSET
        else:
            employment_type = TeachersPensionEmploymentType(_employment_type)




        full_time_salary = d.pop("fullTimeSalary", UNSET)

        part_time_salary_paid = d.pop("partTimeSalaryPaid", UNSET)

        mcr_role_id_1 = d.pop("mcrRoleId1", UNSET)

        mcr_role_id_2 = d.pop("mcrRoleId2", UNSET)

        teachers_pension_admin_ni_number = d.pop("teachersPensionAdminNiNumber", UNSET)

        teachers_pension_details = cls(
            employment_type=employment_type,
            full_time_salary=full_time_salary,
            part_time_salary_paid=part_time_salary_paid,
            mcr_role_id_1=mcr_role_id_1,
            mcr_role_id_2=mcr_role_id_2,
            teachers_pension_admin_ni_number=teachers_pension_admin_ni_number,
        )

        return teachers_pension_details

