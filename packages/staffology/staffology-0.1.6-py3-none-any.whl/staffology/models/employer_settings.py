from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.journal_csv_format import JournalCsvFormat
from ..models.pay_run_entry_warning_type import PayRunEntryWarningType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerSettings")

@attr.s(auto_attribs=True)
class EmployerSettings:
    """Miscellaneous settings related to the employer that don't naturally belong in other models

    Attributes:
        allow_negative_pay (Union[Unset, bool]):
        manual_statutory_pay_lines_enabled (Union[Unset, bool]):
        merge_matching_nominals_enabled (Union[Unset, bool]):
        auto_calc_back_pay_for_new_starters (Union[Unset, bool]):
        pay_code_validation_enabled (Union[Unset, bool]):
        calculate_effective_date_salary_changes (Union[Unset, bool]):
        group_pay_lines_enabled (Union[Unset, bool]): A flag to indicate whether paylines should be grouped. The
            grouping is done based on the following PayLine properties: Rate, Multiplier, Code, Description and RoleId
        contracted_weeks (Union[Unset, float]): The amount of weeks an employee works, utilise for employees who aren't
            working full time.
            This value is the default which can be inherited when creating/updating a WorkingPattern.
        full_time_contracted_weeks (Union[Unset, float]): The amount of weeks an employee works (Full Time).
            This value is the default which can be inherited when creating/updating a WorkingPattern.
        full_time_contracted_hours (Union[Unset, float]): The amount of hours an employee works (Full Time).
            This value is the default which can be inherited when creating/updating a WorkingPattern.
        disabled_pay_run_warnings_list (Union[Unset, None, List[PayRunEntryWarningType]]): Pay run warnings that the
            user has opted to ignore.
        journal_csv_format (Union[Unset, JournalCsvFormat]):
        prefer_async_payrun_api_calls (Union[Unset, bool]): This setting is only available temporarily and is only
            setable by users with access to beta features enabled.
            If set to true the the web applicaiton will use new async API calls for managing payruns
    """

    allow_negative_pay: Union[Unset, bool] = UNSET
    manual_statutory_pay_lines_enabled: Union[Unset, bool] = UNSET
    merge_matching_nominals_enabled: Union[Unset, bool] = UNSET
    auto_calc_back_pay_for_new_starters: Union[Unset, bool] = UNSET
    pay_code_validation_enabled: Union[Unset, bool] = UNSET
    calculate_effective_date_salary_changes: Union[Unset, bool] = UNSET
    group_pay_lines_enabled: Union[Unset, bool] = UNSET
    contracted_weeks: Union[Unset, float] = UNSET
    full_time_contracted_weeks: Union[Unset, float] = UNSET
    full_time_contracted_hours: Union[Unset, float] = UNSET
    disabled_pay_run_warnings_list: Union[Unset, None, List[PayRunEntryWarningType]] = UNSET
    journal_csv_format: Union[Unset, JournalCsvFormat] = UNSET
    prefer_async_payrun_api_calls: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        allow_negative_pay = self.allow_negative_pay
        manual_statutory_pay_lines_enabled = self.manual_statutory_pay_lines_enabled
        merge_matching_nominals_enabled = self.merge_matching_nominals_enabled
        auto_calc_back_pay_for_new_starters = self.auto_calc_back_pay_for_new_starters
        pay_code_validation_enabled = self.pay_code_validation_enabled
        calculate_effective_date_salary_changes = self.calculate_effective_date_salary_changes
        group_pay_lines_enabled = self.group_pay_lines_enabled
        contracted_weeks = self.contracted_weeks
        full_time_contracted_weeks = self.full_time_contracted_weeks
        full_time_contracted_hours = self.full_time_contracted_hours
        disabled_pay_run_warnings_list: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.disabled_pay_run_warnings_list, Unset):
            if self.disabled_pay_run_warnings_list is None:
                disabled_pay_run_warnings_list = None
            else:
                disabled_pay_run_warnings_list = []
                for disabled_pay_run_warnings_list_item_data in self.disabled_pay_run_warnings_list:
                    disabled_pay_run_warnings_list_item = disabled_pay_run_warnings_list_item_data.value

                    disabled_pay_run_warnings_list.append(disabled_pay_run_warnings_list_item)




        journal_csv_format: Union[Unset, str] = UNSET
        if not isinstance(self.journal_csv_format, Unset):
            journal_csv_format = self.journal_csv_format.value

        prefer_async_payrun_api_calls = self.prefer_async_payrun_api_calls

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if allow_negative_pay is not UNSET:
            field_dict["allowNegativePay"] = allow_negative_pay
        if manual_statutory_pay_lines_enabled is not UNSET:
            field_dict["manualStatutoryPayLinesEnabled"] = manual_statutory_pay_lines_enabled
        if merge_matching_nominals_enabled is not UNSET:
            field_dict["mergeMatchingNominalsEnabled"] = merge_matching_nominals_enabled
        if auto_calc_back_pay_for_new_starters is not UNSET:
            field_dict["autoCalcBackPayForNewStarters"] = auto_calc_back_pay_for_new_starters
        if pay_code_validation_enabled is not UNSET:
            field_dict["payCodeValidationEnabled"] = pay_code_validation_enabled
        if calculate_effective_date_salary_changes is not UNSET:
            field_dict["calculateEffectiveDateSalaryChanges"] = calculate_effective_date_salary_changes
        if group_pay_lines_enabled is not UNSET:
            field_dict["groupPayLinesEnabled"] = group_pay_lines_enabled
        if contracted_weeks is not UNSET:
            field_dict["contractedWeeks"] = contracted_weeks
        if full_time_contracted_weeks is not UNSET:
            field_dict["fullTimeContractedWeeks"] = full_time_contracted_weeks
        if full_time_contracted_hours is not UNSET:
            field_dict["fullTimeContractedHours"] = full_time_contracted_hours
        if disabled_pay_run_warnings_list is not UNSET:
            field_dict["disabledPayRunWarningsList"] = disabled_pay_run_warnings_list
        if journal_csv_format is not UNSET:
            field_dict["journalCsvFormat"] = journal_csv_format
        if prefer_async_payrun_api_calls is not UNSET:
            field_dict["preferAsyncPayrunApiCalls"] = prefer_async_payrun_api_calls

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allow_negative_pay = d.pop("allowNegativePay", UNSET)

        manual_statutory_pay_lines_enabled = d.pop("manualStatutoryPayLinesEnabled", UNSET)

        merge_matching_nominals_enabled = d.pop("mergeMatchingNominalsEnabled", UNSET)

        auto_calc_back_pay_for_new_starters = d.pop("autoCalcBackPayForNewStarters", UNSET)

        pay_code_validation_enabled = d.pop("payCodeValidationEnabled", UNSET)

        calculate_effective_date_salary_changes = d.pop("calculateEffectiveDateSalaryChanges", UNSET)

        group_pay_lines_enabled = d.pop("groupPayLinesEnabled", UNSET)

        contracted_weeks = d.pop("contractedWeeks", UNSET)

        full_time_contracted_weeks = d.pop("fullTimeContractedWeeks", UNSET)

        full_time_contracted_hours = d.pop("fullTimeContractedHours", UNSET)

        disabled_pay_run_warnings_list = []
        _disabled_pay_run_warnings_list = d.pop("disabledPayRunWarningsList", UNSET)
        for disabled_pay_run_warnings_list_item_data in (_disabled_pay_run_warnings_list or []):
            disabled_pay_run_warnings_list_item = PayRunEntryWarningType(disabled_pay_run_warnings_list_item_data)



            disabled_pay_run_warnings_list.append(disabled_pay_run_warnings_list_item)


        _journal_csv_format = d.pop("journalCsvFormat", UNSET)
        journal_csv_format: Union[Unset, JournalCsvFormat]
        if isinstance(_journal_csv_format,  Unset):
            journal_csv_format = UNSET
        else:
            journal_csv_format = JournalCsvFormat(_journal_csv_format)




        prefer_async_payrun_api_calls = d.pop("preferAsyncPayrunApiCalls", UNSET)

        employer_settings = cls(
            allow_negative_pay=allow_negative_pay,
            manual_statutory_pay_lines_enabled=manual_statutory_pay_lines_enabled,
            merge_matching_nominals_enabled=merge_matching_nominals_enabled,
            auto_calc_back_pay_for_new_starters=auto_calc_back_pay_for_new_starters,
            pay_code_validation_enabled=pay_code_validation_enabled,
            calculate_effective_date_salary_changes=calculate_effective_date_salary_changes,
            group_pay_lines_enabled=group_pay_lines_enabled,
            contracted_weeks=contracted_weeks,
            full_time_contracted_weeks=full_time_contracted_weeks,
            full_time_contracted_hours=full_time_contracted_hours,
            disabled_pay_run_warnings_list=disabled_pay_run_warnings_list,
            journal_csv_format=journal_csv_format,
            prefer_async_payrun_api_calls=prefer_async_payrun_api_calls,
        )

        return employer_settings

