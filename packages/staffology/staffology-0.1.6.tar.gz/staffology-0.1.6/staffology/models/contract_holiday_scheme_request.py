from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.holiday_scheme_duration_type import HolidaySchemeDurationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractHolidaySchemeRequest")

@attr.s(auto_attribs=True)
class ContractHolidaySchemeRequest:
    """
    Attributes:
        name (str): Holiday scheme name
        average_calculation_weeks (Union[Unset, int]): The number of weeks that the average holiday pay calculation is
            to be calculated over (Default 52)
        use_only_paid_weeks (Union[Unset, bool]): If to go back further than the stated no of weeks for calculation if
            there are weeks where the employee has not been paid. (Default- True)
        ignore_sxp (Union[Unset, bool]): Option to ignore weeks where SXP payments have been paid. The calculation will
            then go back like above until the stated number of weeks are included in the calculation. (Default -True).
        calculation_duration_unit (Union[Unset, HolidaySchemeDurationType]):
        use_ni_pay (Union[Unset, bool]): If use National insurance gross taxable pay. (Default - True).
        use_working_pattern (Union[Unset, bool]): If use the weekly hours or days as per their working pattern as the
            divisor for the average holiday rate.
        pay_code_set_for_pay_id (Union[Unset, None, str]): the Paycode set that they want to use for the Values to
            enable the calculation.
        pay_code_set_for_hours_id (Union[Unset, None, str]): the Paycode set that they want to use for the Hours to
            enable the calculation.
    """

    name: str
    average_calculation_weeks: Union[Unset, int] = UNSET
    use_only_paid_weeks: Union[Unset, bool] = UNSET
    ignore_sxp: Union[Unset, bool] = UNSET
    calculation_duration_unit: Union[Unset, HolidaySchemeDurationType] = UNSET
    use_ni_pay: Union[Unset, bool] = UNSET
    use_working_pattern: Union[Unset, bool] = UNSET
    pay_code_set_for_pay_id: Union[Unset, None, str] = UNSET
    pay_code_set_for_hours_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        average_calculation_weeks = self.average_calculation_weeks
        use_only_paid_weeks = self.use_only_paid_weeks
        ignore_sxp = self.ignore_sxp
        calculation_duration_unit: Union[Unset, str] = UNSET
        if not isinstance(self.calculation_duration_unit, Unset):
            calculation_duration_unit = self.calculation_duration_unit.value

        use_ni_pay = self.use_ni_pay
        use_working_pattern = self.use_working_pattern
        pay_code_set_for_pay_id = self.pay_code_set_for_pay_id
        pay_code_set_for_hours_id = self.pay_code_set_for_hours_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if average_calculation_weeks is not UNSET:
            field_dict["averageCalculationWeeks"] = average_calculation_weeks
        if use_only_paid_weeks is not UNSET:
            field_dict["useOnlyPaidWeeks"] = use_only_paid_weeks
        if ignore_sxp is not UNSET:
            field_dict["ignoreSxp"] = ignore_sxp
        if calculation_duration_unit is not UNSET:
            field_dict["calculationDurationUnit"] = calculation_duration_unit
        if use_ni_pay is not UNSET:
            field_dict["useNiPay"] = use_ni_pay
        if use_working_pattern is not UNSET:
            field_dict["useWorkingPattern"] = use_working_pattern
        if pay_code_set_for_pay_id is not UNSET:
            field_dict["payCodeSetForPayId"] = pay_code_set_for_pay_id
        if pay_code_set_for_hours_id is not UNSET:
            field_dict["payCodeSetForHoursId"] = pay_code_set_for_hours_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        average_calculation_weeks = d.pop("averageCalculationWeeks", UNSET)

        use_only_paid_weeks = d.pop("useOnlyPaidWeeks", UNSET)

        ignore_sxp = d.pop("ignoreSxp", UNSET)

        _calculation_duration_unit = d.pop("calculationDurationUnit", UNSET)
        calculation_duration_unit: Union[Unset, HolidaySchemeDurationType]
        if isinstance(_calculation_duration_unit,  Unset):
            calculation_duration_unit = UNSET
        else:
            calculation_duration_unit = HolidaySchemeDurationType(_calculation_duration_unit)




        use_ni_pay = d.pop("useNiPay", UNSET)

        use_working_pattern = d.pop("useWorkingPattern", UNSET)

        pay_code_set_for_pay_id = d.pop("payCodeSetForPayId", UNSET)

        pay_code_set_for_hours_id = d.pop("payCodeSetForHoursId", UNSET)

        contract_holiday_scheme_request = cls(
            name=name,
            average_calculation_weeks=average_calculation_weeks,
            use_only_paid_weeks=use_only_paid_weeks,
            ignore_sxp=ignore_sxp,
            calculation_duration_unit=calculation_duration_unit,
            use_ni_pay=use_ni_pay,
            use_working_pattern=use_working_pattern,
            pay_code_set_for_pay_id=pay_code_set_for_pay_id,
            pay_code_set_for_hours_id=pay_code_set_for_hours_id,
        )

        return contract_holiday_scheme_request

