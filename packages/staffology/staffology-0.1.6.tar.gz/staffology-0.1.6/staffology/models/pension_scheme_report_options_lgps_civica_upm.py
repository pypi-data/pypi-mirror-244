from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionSchemeReportOptionsLgpsCivicaUpm")

@attr.s(auto_attribs=True)
class PensionSchemeReportOptionsLgpsCivicaUpm:
    """
    Attributes:
        include_folder_no (Union[Unset, bool]):
        pro_rate_pt_hours_weeks_worked (Union[Unset, bool]):
        include_weeks_worked_columns (Union[Unset, bool]):
    """

    include_folder_no: Union[Unset, bool] = UNSET
    pro_rate_pt_hours_weeks_worked: Union[Unset, bool] = UNSET
    include_weeks_worked_columns: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        include_folder_no = self.include_folder_no
        pro_rate_pt_hours_weeks_worked = self.pro_rate_pt_hours_weeks_worked
        include_weeks_worked_columns = self.include_weeks_worked_columns

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if include_folder_no is not UNSET:
            field_dict["includeFolderNo"] = include_folder_no
        if pro_rate_pt_hours_weeks_worked is not UNSET:
            field_dict["proRatePtHoursWeeksWorked"] = pro_rate_pt_hours_weeks_worked
        if include_weeks_worked_columns is not UNSET:
            field_dict["includeWeeksWorkedColumns"] = include_weeks_worked_columns

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include_folder_no = d.pop("includeFolderNo", UNSET)

        pro_rate_pt_hours_weeks_worked = d.pop("proRatePtHoursWeeksWorked", UNSET)

        include_weeks_worked_columns = d.pop("includeWeeksWorkedColumns", UNSET)

        pension_scheme_report_options_lgps_civica_upm = cls(
            include_folder_no=include_folder_no,
            pro_rate_pt_hours_weeks_worked=pro_rate_pt_hours_weeks_worked,
            include_weeks_worked_columns=include_weeks_worked_columns,
        )

        return pension_scheme_report_options_lgps_civica_upm

