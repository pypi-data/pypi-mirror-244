from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.lgps_i_connect_file_type import LgpsIConnectFileType
from ..models.lgps_i_connect_payroll_reference import LgpsIConnectPayrollReference
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionSchemeReportOptionsLgpsIConnect")

@attr.s(auto_attribs=True)
class PensionSchemeReportOptionsLgpsIConnect:
    """
    Attributes:
        file_type (Union[Unset, LgpsIConnectFileType]):
        payroll_reference_1 (Union[Unset, LgpsIConnectPayrollReference]):
        payroll_reference_2 (Union[Unset, LgpsIConnectPayrollReference]):
        payroll_reference_3 (Union[Unset, LgpsIConnectPayrollReference]):
        populate_email_address (Union[Unset, bool]):
        populate_telephone_number (Union[Unset, bool]):
        populate_mobile_number (Union[Unset, bool]):
        populate_works_place_name (Union[Unset, bool]):
        populate_works_address (Union[Unset, bool]):
        populate_works_email_address (Union[Unset, bool]):
        include_employment_breaks (Union[Unset, bool]):
        break_reason_smp_indicator_only (Union[Unset, bool]):
        populate_marital_status (Union[Unset, bool]):
        include_ae_qualifying_earnings (Union[Unset, bool]):
        pro_rate_pt_hours_by_term_time_weeks (Union[Unset, bool]):
        ignore_term_time_weeks_for_fte_final_pay (Union[Unset, bool]):
        show_fte_annual_salary_for_fte_final_pay (Union[Unset, bool]):
    """

    file_type: Union[Unset, LgpsIConnectFileType] = UNSET
    payroll_reference_1: Union[Unset, LgpsIConnectPayrollReference] = UNSET
    payroll_reference_2: Union[Unset, LgpsIConnectPayrollReference] = UNSET
    payroll_reference_3: Union[Unset, LgpsIConnectPayrollReference] = UNSET
    populate_email_address: Union[Unset, bool] = UNSET
    populate_telephone_number: Union[Unset, bool] = UNSET
    populate_mobile_number: Union[Unset, bool] = UNSET
    populate_works_place_name: Union[Unset, bool] = UNSET
    populate_works_address: Union[Unset, bool] = UNSET
    populate_works_email_address: Union[Unset, bool] = UNSET
    include_employment_breaks: Union[Unset, bool] = UNSET
    break_reason_smp_indicator_only: Union[Unset, bool] = UNSET
    populate_marital_status: Union[Unset, bool] = UNSET
    include_ae_qualifying_earnings: Union[Unset, bool] = UNSET
    pro_rate_pt_hours_by_term_time_weeks: Union[Unset, bool] = UNSET
    ignore_term_time_weeks_for_fte_final_pay: Union[Unset, bool] = UNSET
    show_fte_annual_salary_for_fte_final_pay: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        file_type: Union[Unset, str] = UNSET
        if not isinstance(self.file_type, Unset):
            file_type = self.file_type.value

        payroll_reference_1: Union[Unset, str] = UNSET
        if not isinstance(self.payroll_reference_1, Unset):
            payroll_reference_1 = self.payroll_reference_1.value

        payroll_reference_2: Union[Unset, str] = UNSET
        if not isinstance(self.payroll_reference_2, Unset):
            payroll_reference_2 = self.payroll_reference_2.value

        payroll_reference_3: Union[Unset, str] = UNSET
        if not isinstance(self.payroll_reference_3, Unset):
            payroll_reference_3 = self.payroll_reference_3.value

        populate_email_address = self.populate_email_address
        populate_telephone_number = self.populate_telephone_number
        populate_mobile_number = self.populate_mobile_number
        populate_works_place_name = self.populate_works_place_name
        populate_works_address = self.populate_works_address
        populate_works_email_address = self.populate_works_email_address
        include_employment_breaks = self.include_employment_breaks
        break_reason_smp_indicator_only = self.break_reason_smp_indicator_only
        populate_marital_status = self.populate_marital_status
        include_ae_qualifying_earnings = self.include_ae_qualifying_earnings
        pro_rate_pt_hours_by_term_time_weeks = self.pro_rate_pt_hours_by_term_time_weeks
        ignore_term_time_weeks_for_fte_final_pay = self.ignore_term_time_weeks_for_fte_final_pay
        show_fte_annual_salary_for_fte_final_pay = self.show_fte_annual_salary_for_fte_final_pay

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if file_type is not UNSET:
            field_dict["fileType"] = file_type
        if payroll_reference_1 is not UNSET:
            field_dict["payrollReference1"] = payroll_reference_1
        if payroll_reference_2 is not UNSET:
            field_dict["payrollReference2"] = payroll_reference_2
        if payroll_reference_3 is not UNSET:
            field_dict["payrollReference3"] = payroll_reference_3
        if populate_email_address is not UNSET:
            field_dict["populateEmailAddress"] = populate_email_address
        if populate_telephone_number is not UNSET:
            field_dict["populateTelephoneNumber"] = populate_telephone_number
        if populate_mobile_number is not UNSET:
            field_dict["populateMobileNumber"] = populate_mobile_number
        if populate_works_place_name is not UNSET:
            field_dict["populateWorksPlaceName"] = populate_works_place_name
        if populate_works_address is not UNSET:
            field_dict["populateWorksAddress"] = populate_works_address
        if populate_works_email_address is not UNSET:
            field_dict["populateWorksEmailAddress"] = populate_works_email_address
        if include_employment_breaks is not UNSET:
            field_dict["includeEmploymentBreaks"] = include_employment_breaks
        if break_reason_smp_indicator_only is not UNSET:
            field_dict["breakReasonSmpIndicatorOnly"] = break_reason_smp_indicator_only
        if populate_marital_status is not UNSET:
            field_dict["populateMaritalStatus"] = populate_marital_status
        if include_ae_qualifying_earnings is not UNSET:
            field_dict["includeAeQualifyingEarnings"] = include_ae_qualifying_earnings
        if pro_rate_pt_hours_by_term_time_weeks is not UNSET:
            field_dict["proRatePtHoursByTermTimeWeeks"] = pro_rate_pt_hours_by_term_time_weeks
        if ignore_term_time_weeks_for_fte_final_pay is not UNSET:
            field_dict["ignoreTermTimeWeeksForFteFinalPay"] = ignore_term_time_weeks_for_fte_final_pay
        if show_fte_annual_salary_for_fte_final_pay is not UNSET:
            field_dict["showFteAnnualSalaryForFteFinalPay"] = show_fte_annual_salary_for_fte_final_pay

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _file_type = d.pop("fileType", UNSET)
        file_type: Union[Unset, LgpsIConnectFileType]
        if isinstance(_file_type,  Unset):
            file_type = UNSET
        else:
            file_type = LgpsIConnectFileType(_file_type)




        _payroll_reference_1 = d.pop("payrollReference1", UNSET)
        payroll_reference_1: Union[Unset, LgpsIConnectPayrollReference]
        if isinstance(_payroll_reference_1,  Unset):
            payroll_reference_1 = UNSET
        else:
            payroll_reference_1 = LgpsIConnectPayrollReference(_payroll_reference_1)




        _payroll_reference_2 = d.pop("payrollReference2", UNSET)
        payroll_reference_2: Union[Unset, LgpsIConnectPayrollReference]
        if isinstance(_payroll_reference_2,  Unset):
            payroll_reference_2 = UNSET
        else:
            payroll_reference_2 = LgpsIConnectPayrollReference(_payroll_reference_2)




        _payroll_reference_3 = d.pop("payrollReference3", UNSET)
        payroll_reference_3: Union[Unset, LgpsIConnectPayrollReference]
        if isinstance(_payroll_reference_3,  Unset):
            payroll_reference_3 = UNSET
        else:
            payroll_reference_3 = LgpsIConnectPayrollReference(_payroll_reference_3)




        populate_email_address = d.pop("populateEmailAddress", UNSET)

        populate_telephone_number = d.pop("populateTelephoneNumber", UNSET)

        populate_mobile_number = d.pop("populateMobileNumber", UNSET)

        populate_works_place_name = d.pop("populateWorksPlaceName", UNSET)

        populate_works_address = d.pop("populateWorksAddress", UNSET)

        populate_works_email_address = d.pop("populateWorksEmailAddress", UNSET)

        include_employment_breaks = d.pop("includeEmploymentBreaks", UNSET)

        break_reason_smp_indicator_only = d.pop("breakReasonSmpIndicatorOnly", UNSET)

        populate_marital_status = d.pop("populateMaritalStatus", UNSET)

        include_ae_qualifying_earnings = d.pop("includeAeQualifyingEarnings", UNSET)

        pro_rate_pt_hours_by_term_time_weeks = d.pop("proRatePtHoursByTermTimeWeeks", UNSET)

        ignore_term_time_weeks_for_fte_final_pay = d.pop("ignoreTermTimeWeeksForFteFinalPay", UNSET)

        show_fte_annual_salary_for_fte_final_pay = d.pop("showFteAnnualSalaryForFteFinalPay", UNSET)

        pension_scheme_report_options_lgps_i_connect = cls(
            file_type=file_type,
            payroll_reference_1=payroll_reference_1,
            payroll_reference_2=payroll_reference_2,
            payroll_reference_3=payroll_reference_3,
            populate_email_address=populate_email_address,
            populate_telephone_number=populate_telephone_number,
            populate_mobile_number=populate_mobile_number,
            populate_works_place_name=populate_works_place_name,
            populate_works_address=populate_works_address,
            populate_works_email_address=populate_works_email_address,
            include_employment_breaks=include_employment_breaks,
            break_reason_smp_indicator_only=break_reason_smp_indicator_only,
            populate_marital_status=populate_marital_status,
            include_ae_qualifying_earnings=include_ae_qualifying_earnings,
            pro_rate_pt_hours_by_term_time_weeks=pro_rate_pt_hours_by_term_time_weeks,
            ignore_term_time_weeks_for_fte_final_pay=ignore_term_time_weeks_for_fte_final_pay,
            show_fte_annual_salary_for_fte_final_pay=show_fte_annual_salary_for_fte_final_pay,
        )

        return pension_scheme_report_options_lgps_i_connect

