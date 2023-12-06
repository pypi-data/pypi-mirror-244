from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.bank_holiday_collection import BankHolidayCollection
from ..models.pro_rata_rule import ProRataRule
from ..models.working_pattern_hours_type import WorkingPatternHoursType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractWorkingPatternRequest")

@attr.s(auto_attribs=True)
class ContractWorkingPatternRequest:
    """
    Attributes:
        title (str):
        id (Union[Unset, str]):
        mon (Union[Unset, float]):
        tue (Union[Unset, float]):
        wed (Union[Unset, float]):
        thu (Union[Unset, float]):
        fri (Union[Unset, float]):
        sat (Union[Unset, float]):
        sun (Union[Unset, float]):
        mon_is_working_day (Union[Unset, bool]):
        tue_is_working_day (Union[Unset, bool]):
        wed_is_working_day (Union[Unset, bool]):
        thu_is_working_day (Union[Unset, bool]):
        fri_is_working_day (Union[Unset, bool]):
        sat_is_working_day (Union[Unset, bool]):
        sun_is_working_day (Union[Unset, bool]):
        total_hours (Union[Unset, float]):
        contracted_weeks (Union[Unset, None, float]): The amount of weeks an employee works, utilise for employees who
            aren't working full time.
            If Null then the default is used.
        full_time_contracted_weeks (Union[Unset, None, float]): The amount of weeks an employee works (Full Time). If
            Null then the default is used.
        full_time_contracted_hours (Union[Unset, None, float]): The amount of hours an employee works (Full Time). If
            Null then the default is used.
        bank_holidays (Union[Unset, BankHolidayCollection]):
        pro_rata_rule (Union[Unset, ProRataRule]):
        working_pattern_hours_type (Union[Unset, WorkingPatternHoursType]):
        is_default (Union[Unset, bool]):
    """

    title: str
    id: Union[Unset, str] = UNSET
    mon: Union[Unset, float] = UNSET
    tue: Union[Unset, float] = UNSET
    wed: Union[Unset, float] = UNSET
    thu: Union[Unset, float] = UNSET
    fri: Union[Unset, float] = UNSET
    sat: Union[Unset, float] = UNSET
    sun: Union[Unset, float] = UNSET
    mon_is_working_day: Union[Unset, bool] = UNSET
    tue_is_working_day: Union[Unset, bool] = UNSET
    wed_is_working_day: Union[Unset, bool] = UNSET
    thu_is_working_day: Union[Unset, bool] = UNSET
    fri_is_working_day: Union[Unset, bool] = UNSET
    sat_is_working_day: Union[Unset, bool] = UNSET
    sun_is_working_day: Union[Unset, bool] = UNSET
    total_hours: Union[Unset, float] = UNSET
    contracted_weeks: Union[Unset, None, float] = UNSET
    full_time_contracted_weeks: Union[Unset, None, float] = UNSET
    full_time_contracted_hours: Union[Unset, None, float] = UNSET
    bank_holidays: Union[Unset, BankHolidayCollection] = UNSET
    pro_rata_rule: Union[Unset, ProRataRule] = UNSET
    working_pattern_hours_type: Union[Unset, WorkingPatternHoursType] = UNSET
    is_default: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        id = self.id
        mon = self.mon
        tue = self.tue
        wed = self.wed
        thu = self.thu
        fri = self.fri
        sat = self.sat
        sun = self.sun
        mon_is_working_day = self.mon_is_working_day
        tue_is_working_day = self.tue_is_working_day
        wed_is_working_day = self.wed_is_working_day
        thu_is_working_day = self.thu_is_working_day
        fri_is_working_day = self.fri_is_working_day
        sat_is_working_day = self.sat_is_working_day
        sun_is_working_day = self.sun_is_working_day
        total_hours = self.total_hours
        contracted_weeks = self.contracted_weeks
        full_time_contracted_weeks = self.full_time_contracted_weeks
        full_time_contracted_hours = self.full_time_contracted_hours
        bank_holidays: Union[Unset, str] = UNSET
        if not isinstance(self.bank_holidays, Unset):
            bank_holidays = self.bank_holidays.value

        pro_rata_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pro_rata_rule, Unset):
            pro_rata_rule = self.pro_rata_rule.value

        working_pattern_hours_type: Union[Unset, str] = UNSET
        if not isinstance(self.working_pattern_hours_type, Unset):
            working_pattern_hours_type = self.working_pattern_hours_type.value

        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "title": title,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if mon is not UNSET:
            field_dict["mon"] = mon
        if tue is not UNSET:
            field_dict["tue"] = tue
        if wed is not UNSET:
            field_dict["wed"] = wed
        if thu is not UNSET:
            field_dict["thu"] = thu
        if fri is not UNSET:
            field_dict["fri"] = fri
        if sat is not UNSET:
            field_dict["sat"] = sat
        if sun is not UNSET:
            field_dict["sun"] = sun
        if mon_is_working_day is not UNSET:
            field_dict["monIsWorkingDay"] = mon_is_working_day
        if tue_is_working_day is not UNSET:
            field_dict["tueIsWorkingDay"] = tue_is_working_day
        if wed_is_working_day is not UNSET:
            field_dict["wedIsWorkingDay"] = wed_is_working_day
        if thu_is_working_day is not UNSET:
            field_dict["thuIsWorkingDay"] = thu_is_working_day
        if fri_is_working_day is not UNSET:
            field_dict["friIsWorkingDay"] = fri_is_working_day
        if sat_is_working_day is not UNSET:
            field_dict["satIsWorkingDay"] = sat_is_working_day
        if sun_is_working_day is not UNSET:
            field_dict["sunIsWorkingDay"] = sun_is_working_day
        if total_hours is not UNSET:
            field_dict["totalHours"] = total_hours
        if contracted_weeks is not UNSET:
            field_dict["contractedWeeks"] = contracted_weeks
        if full_time_contracted_weeks is not UNSET:
            field_dict["fullTimeContractedWeeks"] = full_time_contracted_weeks
        if full_time_contracted_hours is not UNSET:
            field_dict["fullTimeContractedHours"] = full_time_contracted_hours
        if bank_holidays is not UNSET:
            field_dict["bankHolidays"] = bank_holidays
        if pro_rata_rule is not UNSET:
            field_dict["proRataRule"] = pro_rata_rule
        if working_pattern_hours_type is not UNSET:
            field_dict["workingPatternHoursType"] = working_pattern_hours_type
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        id = d.pop("id", UNSET)

        mon = d.pop("mon", UNSET)

        tue = d.pop("tue", UNSET)

        wed = d.pop("wed", UNSET)

        thu = d.pop("thu", UNSET)

        fri = d.pop("fri", UNSET)

        sat = d.pop("sat", UNSET)

        sun = d.pop("sun", UNSET)

        mon_is_working_day = d.pop("monIsWorkingDay", UNSET)

        tue_is_working_day = d.pop("tueIsWorkingDay", UNSET)

        wed_is_working_day = d.pop("wedIsWorkingDay", UNSET)

        thu_is_working_day = d.pop("thuIsWorkingDay", UNSET)

        fri_is_working_day = d.pop("friIsWorkingDay", UNSET)

        sat_is_working_day = d.pop("satIsWorkingDay", UNSET)

        sun_is_working_day = d.pop("sunIsWorkingDay", UNSET)

        total_hours = d.pop("totalHours", UNSET)

        contracted_weeks = d.pop("contractedWeeks", UNSET)

        full_time_contracted_weeks = d.pop("fullTimeContractedWeeks", UNSET)

        full_time_contracted_hours = d.pop("fullTimeContractedHours", UNSET)

        _bank_holidays = d.pop("bankHolidays", UNSET)
        bank_holidays: Union[Unset, BankHolidayCollection]
        if isinstance(_bank_holidays,  Unset):
            bank_holidays = UNSET
        else:
            bank_holidays = BankHolidayCollection(_bank_holidays)




        _pro_rata_rule = d.pop("proRataRule", UNSET)
        pro_rata_rule: Union[Unset, ProRataRule]
        if isinstance(_pro_rata_rule,  Unset):
            pro_rata_rule = UNSET
        else:
            pro_rata_rule = ProRataRule(_pro_rata_rule)




        _working_pattern_hours_type = d.pop("workingPatternHoursType", UNSET)
        working_pattern_hours_type: Union[Unset, WorkingPatternHoursType]
        if isinstance(_working_pattern_hours_type,  Unset):
            working_pattern_hours_type = UNSET
        else:
            working_pattern_hours_type = WorkingPatternHoursType(_working_pattern_hours_type)




        is_default = d.pop("isDefault", UNSET)

        contract_working_pattern_request = cls(
            title=title,
            id=id,
            mon=mon,
            tue=tue,
            wed=wed,
            thu=thu,
            fri=fri,
            sat=sat,
            sun=sun,
            mon_is_working_day=mon_is_working_day,
            tue_is_working_day=tue_is_working_day,
            wed_is_working_day=wed_is_working_day,
            thu_is_working_day=thu_is_working_day,
            fri_is_working_day=fri_is_working_day,
            sat_is_working_day=sat_is_working_day,
            sun_is_working_day=sun_is_working_day,
            total_hours=total_hours,
            contracted_weeks=contracted_weeks,
            full_time_contracted_weeks=full_time_contracted_weeks,
            full_time_contracted_hours=full_time_contracted_hours,
            bank_holidays=bank_holidays,
            pro_rata_rule=pro_rata_rule,
            working_pattern_hours_type=working_pattern_hours_type,
            is_default=is_default,
        )

        return contract_working_pattern_request

