import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.holiday_accrual import HolidayAccrual
from ..models.holiday_accrual_default_rate_type import HolidayAccrualDefaultRateType
from ..models.holiday_type import HolidayType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractLeaveSettingsResponse")

@attr.s(auto_attribs=True)
class ContractLeaveSettingsResponse:
    """
    Attributes:
        allowance_used (Union[Unset, float]): [readonly] The number of days used from the allowance since last reset
        allowance_used_previous_period (Union[Unset, float]): [readonly] The number of days used in the 12 months prior
            to the last reset
        allowance_remaining (Union[Unset, float]): [readonly] The number of days remaining of the allowance until next
            reset
        accrued_payment_liability (Union[Unset, float]): [readonly] The total accrued payments for this employee over
            the lifetime of their employment so far
        accrued_payment_paid (Union[Unset, float]): [readonly] The Total amount paid to this employee in lieu of
            holidays
        accrued_payment_balance (Union[Unset, float]): [readonly] The balance of what is owed to this employee in lieu
            of holidays
        accrued_hours_amount (Union[Unset, float]): [readonly] The total accrued hours for this employee over the
            lifetime of their employment so far
        accrued_hours_paid (Union[Unset, float]): [readonly] The Total amount of hours paid to this employee in lieu of
            holidays
        accrued_hours_balance (Union[Unset, float]): [readonly] The balance of hours owed to this employee in lieu of
            holidays
        use_default_holiday_type (Union[Unset, bool]): If true then the value for HolidayType comes from the Employer
            record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_allowance_reset_date (Union[Unset, bool]): If true then the value for the AllowanceResetDate comes
            from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_allowance (Union[Unset, bool]): If true then the value for the Allowance comes from the Employer
            record.
            This property only appears if the LeaveSettings if a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu (Union[Unset, bool]): If true then the value for AccruePaymentInLieu comes
            from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_rate (Union[Unset, bool]): If true then the value for AccruePaymentInLieuRate
            comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_all_gross_pay (Union[Unset, bool]): If true then the value for
            AccruePaymentInLieuAllGrossPay comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_pay_automatically (Union[Unset, bool]): If true then the value for
            AccruePaymentInLieu comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_hours_per_day (Union[Unset, bool]): If true then the value for AccrueHoursPerDay comes from
            the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_maximum_accrue_period (Union[Unset, bool]): If true then the value for MaximumAccruePeriod comes
            from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        allowance_reset_date (Union[Unset, datetime.date]): The date that the holiday allowance resets. Only the
            day/month part of the value is relevant.
        allowance (Union[Unset, float]): The number of days holiday an employee can take per year if HolidayType is
            Days.
            Otherwise this is readonly and gives you the number of days accrued since the last reset
        adjustment (Union[Unset, None, float]): Adjustment to number of hours/days/weeks holiday this employee can take
            per year.
            Will reset to 0 when the Allowance resets.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        holiday_type (Union[Unset, HolidayType]):
        accrue_set_amount (Union[Unset, bool]): If true and HolidayType is Accrual_Days then the AccruePaymentInLieuRate
            will be treated as the set amount to accrue per period worked.
        accrue_hours_per_day (Union[Unset, float]): If HolidayType is Accrual_Days then this value is used to help
            convert hours worked into days accrued
        show_allowance_on_payslip (Union[Unset, bool]): If true then the remaining Allowance will be shown on the
            employees payslip.
        show_ahp_on_payslip (Union[Unset, bool]): If true then the AHP balance will be shown on the employees payslip.
        accrue_payment_in_lieu_rate (Union[Unset, float]): The rate at which Payments in Lieu acrrue. Typically this
            should be 12.07%.
        accrue_payment_in_lieu_all_gross_pay (Union[Unset, bool]): Set to true if you want accrued holiday payments to
            be calculated on the total gross pay for the employee or just on the single regular pay element
        accrue_payment_in_lieu_pay_automatically (Union[Unset, bool]): Set to true if you want employees to be
            automatically paid any outstanding holiday pay
        occupational_sickness_unique_id (Union[Unset, None, str]):
        accrued_payment_adjustment (Union[Unset, float]): Any manual adjustment to the total accrued
        accrued_hours_adjustment (Union[Unset, float]): Any manual adjustment to the total hours accrued
        holiday_accrual_basis (Union[Unset, HolidayAccrual]):
        holiday_accrual_default_rate_type (Union[Unset, HolidayAccrualDefaultRateType]):
        aggregated_service_date (Union[Unset, None, datetime.date]):
        use_aggregated_service_date (Union[Unset, bool]):
        accrue_pay_code_set_unique_id (Union[Unset, None, str]): Pay code set to use for accruing holiday pay
        maximum_accrue_period (Union[Unset, None, float]): The maximum number of hours capable of being accrued in a
            single period
    """

    allowance_used: Union[Unset, float] = UNSET
    allowance_used_previous_period: Union[Unset, float] = UNSET
    allowance_remaining: Union[Unset, float] = UNSET
    accrued_payment_liability: Union[Unset, float] = UNSET
    accrued_payment_paid: Union[Unset, float] = UNSET
    accrued_payment_balance: Union[Unset, float] = UNSET
    accrued_hours_amount: Union[Unset, float] = UNSET
    accrued_hours_paid: Union[Unset, float] = UNSET
    accrued_hours_balance: Union[Unset, float] = UNSET
    use_default_holiday_type: Union[Unset, bool] = UNSET
    use_default_allowance_reset_date: Union[Unset, bool] = UNSET
    use_default_allowance: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_rate: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_all_gross_pay: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_pay_automatically: Union[Unset, bool] = UNSET
    use_default_accrue_hours_per_day: Union[Unset, bool] = UNSET
    use_default_maximum_accrue_period: Union[Unset, bool] = UNSET
    allowance_reset_date: Union[Unset, datetime.date] = UNSET
    allowance: Union[Unset, float] = UNSET
    adjustment: Union[Unset, None, float] = UNSET
    holiday_type: Union[Unset, HolidayType] = UNSET
    accrue_set_amount: Union[Unset, bool] = UNSET
    accrue_hours_per_day: Union[Unset, float] = UNSET
    show_allowance_on_payslip: Union[Unset, bool] = UNSET
    show_ahp_on_payslip: Union[Unset, bool] = UNSET
    accrue_payment_in_lieu_rate: Union[Unset, float] = UNSET
    accrue_payment_in_lieu_all_gross_pay: Union[Unset, bool] = UNSET
    accrue_payment_in_lieu_pay_automatically: Union[Unset, bool] = UNSET
    occupational_sickness_unique_id: Union[Unset, None, str] = UNSET
    accrued_payment_adjustment: Union[Unset, float] = UNSET
    accrued_hours_adjustment: Union[Unset, float] = UNSET
    holiday_accrual_basis: Union[Unset, HolidayAccrual] = UNSET
    holiday_accrual_default_rate_type: Union[Unset, HolidayAccrualDefaultRateType] = UNSET
    aggregated_service_date: Union[Unset, None, datetime.date] = UNSET
    use_aggregated_service_date: Union[Unset, bool] = UNSET
    accrue_pay_code_set_unique_id: Union[Unset, None, str] = UNSET
    maximum_accrue_period: Union[Unset, None, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        allowance_used = self.allowance_used
        allowance_used_previous_period = self.allowance_used_previous_period
        allowance_remaining = self.allowance_remaining
        accrued_payment_liability = self.accrued_payment_liability
        accrued_payment_paid = self.accrued_payment_paid
        accrued_payment_balance = self.accrued_payment_balance
        accrued_hours_amount = self.accrued_hours_amount
        accrued_hours_paid = self.accrued_hours_paid
        accrued_hours_balance = self.accrued_hours_balance
        use_default_holiday_type = self.use_default_holiday_type
        use_default_allowance_reset_date = self.use_default_allowance_reset_date
        use_default_allowance = self.use_default_allowance
        use_default_accrue_payment_in_lieu = self.use_default_accrue_payment_in_lieu
        use_default_accrue_payment_in_lieu_rate = self.use_default_accrue_payment_in_lieu_rate
        use_default_accrue_payment_in_lieu_all_gross_pay = self.use_default_accrue_payment_in_lieu_all_gross_pay
        use_default_accrue_payment_in_lieu_pay_automatically = self.use_default_accrue_payment_in_lieu_pay_automatically
        use_default_accrue_hours_per_day = self.use_default_accrue_hours_per_day
        use_default_maximum_accrue_period = self.use_default_maximum_accrue_period
        allowance_reset_date: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_reset_date, Unset):
            allowance_reset_date = self.allowance_reset_date.isoformat()

        allowance = self.allowance
        adjustment = self.adjustment
        holiday_type: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_type, Unset):
            holiday_type = self.holiday_type.value

        accrue_set_amount = self.accrue_set_amount
        accrue_hours_per_day = self.accrue_hours_per_day
        show_allowance_on_payslip = self.show_allowance_on_payslip
        show_ahp_on_payslip = self.show_ahp_on_payslip
        accrue_payment_in_lieu_rate = self.accrue_payment_in_lieu_rate
        accrue_payment_in_lieu_all_gross_pay = self.accrue_payment_in_lieu_all_gross_pay
        accrue_payment_in_lieu_pay_automatically = self.accrue_payment_in_lieu_pay_automatically
        occupational_sickness_unique_id = self.occupational_sickness_unique_id
        accrued_payment_adjustment = self.accrued_payment_adjustment
        accrued_hours_adjustment = self.accrued_hours_adjustment
        holiday_accrual_basis: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_accrual_basis, Unset):
            holiday_accrual_basis = self.holiday_accrual_basis.value

        holiday_accrual_default_rate_type: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_accrual_default_rate_type, Unset):
            holiday_accrual_default_rate_type = self.holiday_accrual_default_rate_type.value

        aggregated_service_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.aggregated_service_date, Unset):
            aggregated_service_date = self.aggregated_service_date.isoformat() if self.aggregated_service_date else None

        use_aggregated_service_date = self.use_aggregated_service_date
        accrue_pay_code_set_unique_id = self.accrue_pay_code_set_unique_id
        maximum_accrue_period = self.maximum_accrue_period

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if allowance_used is not UNSET:
            field_dict["allowanceUsed"] = allowance_used
        if allowance_used_previous_period is not UNSET:
            field_dict["allowanceUsedPreviousPeriod"] = allowance_used_previous_period
        if allowance_remaining is not UNSET:
            field_dict["allowanceRemaining"] = allowance_remaining
        if accrued_payment_liability is not UNSET:
            field_dict["accruedPaymentLiability"] = accrued_payment_liability
        if accrued_payment_paid is not UNSET:
            field_dict["accruedPaymentPaid"] = accrued_payment_paid
        if accrued_payment_balance is not UNSET:
            field_dict["accruedPaymentBalance"] = accrued_payment_balance
        if accrued_hours_amount is not UNSET:
            field_dict["accruedHoursAmount"] = accrued_hours_amount
        if accrued_hours_paid is not UNSET:
            field_dict["accruedHoursPaid"] = accrued_hours_paid
        if accrued_hours_balance is not UNSET:
            field_dict["accruedHoursBalance"] = accrued_hours_balance
        if use_default_holiday_type is not UNSET:
            field_dict["useDefaultHolidayType"] = use_default_holiday_type
        if use_default_allowance_reset_date is not UNSET:
            field_dict["useDefaultAllowanceResetDate"] = use_default_allowance_reset_date
        if use_default_allowance is not UNSET:
            field_dict["useDefaultAllowance"] = use_default_allowance
        if use_default_accrue_payment_in_lieu is not UNSET:
            field_dict["useDefaultAccruePaymentInLieu"] = use_default_accrue_payment_in_lieu
        if use_default_accrue_payment_in_lieu_rate is not UNSET:
            field_dict["useDefaultAccruePaymentInLieuRate"] = use_default_accrue_payment_in_lieu_rate
        if use_default_accrue_payment_in_lieu_all_gross_pay is not UNSET:
            field_dict["useDefaultAccruePaymentInLieuAllGrossPay"] = use_default_accrue_payment_in_lieu_all_gross_pay
        if use_default_accrue_payment_in_lieu_pay_automatically is not UNSET:
            field_dict["useDefaultAccruePaymentInLieuPayAutomatically"] = use_default_accrue_payment_in_lieu_pay_automatically
        if use_default_accrue_hours_per_day is not UNSET:
            field_dict["useDefaultAccrueHoursPerDay"] = use_default_accrue_hours_per_day
        if use_default_maximum_accrue_period is not UNSET:
            field_dict["useDefaultMaximumAccruePeriod"] = use_default_maximum_accrue_period
        if allowance_reset_date is not UNSET:
            field_dict["allowanceResetDate"] = allowance_reset_date
        if allowance is not UNSET:
            field_dict["allowance"] = allowance
        if adjustment is not UNSET:
            field_dict["adjustment"] = adjustment
        if holiday_type is not UNSET:
            field_dict["holidayType"] = holiday_type
        if accrue_set_amount is not UNSET:
            field_dict["accrueSetAmount"] = accrue_set_amount
        if accrue_hours_per_day is not UNSET:
            field_dict["accrueHoursPerDay"] = accrue_hours_per_day
        if show_allowance_on_payslip is not UNSET:
            field_dict["showAllowanceOnPayslip"] = show_allowance_on_payslip
        if show_ahp_on_payslip is not UNSET:
            field_dict["showAhpOnPayslip"] = show_ahp_on_payslip
        if accrue_payment_in_lieu_rate is not UNSET:
            field_dict["accruePaymentInLieuRate"] = accrue_payment_in_lieu_rate
        if accrue_payment_in_lieu_all_gross_pay is not UNSET:
            field_dict["accruePaymentInLieuAllGrossPay"] = accrue_payment_in_lieu_all_gross_pay
        if accrue_payment_in_lieu_pay_automatically is not UNSET:
            field_dict["accruePaymentInLieuPayAutomatically"] = accrue_payment_in_lieu_pay_automatically
        if occupational_sickness_unique_id is not UNSET:
            field_dict["occupationalSicknessUniqueId"] = occupational_sickness_unique_id
        if accrued_payment_adjustment is not UNSET:
            field_dict["accruedPaymentAdjustment"] = accrued_payment_adjustment
        if accrued_hours_adjustment is not UNSET:
            field_dict["accruedHoursAdjustment"] = accrued_hours_adjustment
        if holiday_accrual_basis is not UNSET:
            field_dict["holidayAccrualBasis"] = holiday_accrual_basis
        if holiday_accrual_default_rate_type is not UNSET:
            field_dict["holidayAccrualDefaultRateType"] = holiday_accrual_default_rate_type
        if aggregated_service_date is not UNSET:
            field_dict["aggregatedServiceDate"] = aggregated_service_date
        if use_aggregated_service_date is not UNSET:
            field_dict["useAggregatedServiceDate"] = use_aggregated_service_date
        if accrue_pay_code_set_unique_id is not UNSET:
            field_dict["accruePayCodeSetUniqueId"] = accrue_pay_code_set_unique_id
        if maximum_accrue_period is not UNSET:
            field_dict["maximumAccruePeriod"] = maximum_accrue_period

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allowance_used = d.pop("allowanceUsed", UNSET)

        allowance_used_previous_period = d.pop("allowanceUsedPreviousPeriod", UNSET)

        allowance_remaining = d.pop("allowanceRemaining", UNSET)

        accrued_payment_liability = d.pop("accruedPaymentLiability", UNSET)

        accrued_payment_paid = d.pop("accruedPaymentPaid", UNSET)

        accrued_payment_balance = d.pop("accruedPaymentBalance", UNSET)

        accrued_hours_amount = d.pop("accruedHoursAmount", UNSET)

        accrued_hours_paid = d.pop("accruedHoursPaid", UNSET)

        accrued_hours_balance = d.pop("accruedHoursBalance", UNSET)

        use_default_holiday_type = d.pop("useDefaultHolidayType", UNSET)

        use_default_allowance_reset_date = d.pop("useDefaultAllowanceResetDate", UNSET)

        use_default_allowance = d.pop("useDefaultAllowance", UNSET)

        use_default_accrue_payment_in_lieu = d.pop("useDefaultAccruePaymentInLieu", UNSET)

        use_default_accrue_payment_in_lieu_rate = d.pop("useDefaultAccruePaymentInLieuRate", UNSET)

        use_default_accrue_payment_in_lieu_all_gross_pay = d.pop("useDefaultAccruePaymentInLieuAllGrossPay", UNSET)

        use_default_accrue_payment_in_lieu_pay_automatically = d.pop("useDefaultAccruePaymentInLieuPayAutomatically", UNSET)

        use_default_accrue_hours_per_day = d.pop("useDefaultAccrueHoursPerDay", UNSET)

        use_default_maximum_accrue_period = d.pop("useDefaultMaximumAccruePeriod", UNSET)

        _allowance_reset_date = d.pop("allowanceResetDate", UNSET)
        allowance_reset_date: Union[Unset, datetime.date]
        if isinstance(_allowance_reset_date,  Unset):
            allowance_reset_date = UNSET
        else:
            allowance_reset_date = isoparse(_allowance_reset_date).date()




        allowance = d.pop("allowance", UNSET)

        adjustment = d.pop("adjustment", UNSET)

        _holiday_type = d.pop("holidayType", UNSET)
        holiday_type: Union[Unset, HolidayType]
        if isinstance(_holiday_type,  Unset):
            holiday_type = UNSET
        else:
            holiday_type = HolidayType(_holiday_type)




        accrue_set_amount = d.pop("accrueSetAmount", UNSET)

        accrue_hours_per_day = d.pop("accrueHoursPerDay", UNSET)

        show_allowance_on_payslip = d.pop("showAllowanceOnPayslip", UNSET)

        show_ahp_on_payslip = d.pop("showAhpOnPayslip", UNSET)

        accrue_payment_in_lieu_rate = d.pop("accruePaymentInLieuRate", UNSET)

        accrue_payment_in_lieu_all_gross_pay = d.pop("accruePaymentInLieuAllGrossPay", UNSET)

        accrue_payment_in_lieu_pay_automatically = d.pop("accruePaymentInLieuPayAutomatically", UNSET)

        occupational_sickness_unique_id = d.pop("occupationalSicknessUniqueId", UNSET)

        accrued_payment_adjustment = d.pop("accruedPaymentAdjustment", UNSET)

        accrued_hours_adjustment = d.pop("accruedHoursAdjustment", UNSET)

        _holiday_accrual_basis = d.pop("holidayAccrualBasis", UNSET)
        holiday_accrual_basis: Union[Unset, HolidayAccrual]
        if isinstance(_holiday_accrual_basis,  Unset):
            holiday_accrual_basis = UNSET
        else:
            holiday_accrual_basis = HolidayAccrual(_holiday_accrual_basis)




        _holiday_accrual_default_rate_type = d.pop("holidayAccrualDefaultRateType", UNSET)
        holiday_accrual_default_rate_type: Union[Unset, HolidayAccrualDefaultRateType]
        if isinstance(_holiday_accrual_default_rate_type,  Unset):
            holiday_accrual_default_rate_type = UNSET
        else:
            holiday_accrual_default_rate_type = HolidayAccrualDefaultRateType(_holiday_accrual_default_rate_type)




        _aggregated_service_date = d.pop("aggregatedServiceDate", UNSET)
        aggregated_service_date: Union[Unset, None, datetime.date]
        if _aggregated_service_date is None:
            aggregated_service_date = None
        elif isinstance(_aggregated_service_date,  Unset):
            aggregated_service_date = UNSET
        else:
            aggregated_service_date = isoparse(_aggregated_service_date).date()




        use_aggregated_service_date = d.pop("useAggregatedServiceDate", UNSET)

        accrue_pay_code_set_unique_id = d.pop("accruePayCodeSetUniqueId", UNSET)

        maximum_accrue_period = d.pop("maximumAccruePeriod", UNSET)

        contract_leave_settings_response = cls(
            allowance_used=allowance_used,
            allowance_used_previous_period=allowance_used_previous_period,
            allowance_remaining=allowance_remaining,
            accrued_payment_liability=accrued_payment_liability,
            accrued_payment_paid=accrued_payment_paid,
            accrued_payment_balance=accrued_payment_balance,
            accrued_hours_amount=accrued_hours_amount,
            accrued_hours_paid=accrued_hours_paid,
            accrued_hours_balance=accrued_hours_balance,
            use_default_holiday_type=use_default_holiday_type,
            use_default_allowance_reset_date=use_default_allowance_reset_date,
            use_default_allowance=use_default_allowance,
            use_default_accrue_payment_in_lieu=use_default_accrue_payment_in_lieu,
            use_default_accrue_payment_in_lieu_rate=use_default_accrue_payment_in_lieu_rate,
            use_default_accrue_payment_in_lieu_all_gross_pay=use_default_accrue_payment_in_lieu_all_gross_pay,
            use_default_accrue_payment_in_lieu_pay_automatically=use_default_accrue_payment_in_lieu_pay_automatically,
            use_default_accrue_hours_per_day=use_default_accrue_hours_per_day,
            use_default_maximum_accrue_period=use_default_maximum_accrue_period,
            allowance_reset_date=allowance_reset_date,
            allowance=allowance,
            adjustment=adjustment,
            holiday_type=holiday_type,
            accrue_set_amount=accrue_set_amount,
            accrue_hours_per_day=accrue_hours_per_day,
            show_allowance_on_payslip=show_allowance_on_payslip,
            show_ahp_on_payslip=show_ahp_on_payslip,
            accrue_payment_in_lieu_rate=accrue_payment_in_lieu_rate,
            accrue_payment_in_lieu_all_gross_pay=accrue_payment_in_lieu_all_gross_pay,
            accrue_payment_in_lieu_pay_automatically=accrue_payment_in_lieu_pay_automatically,
            occupational_sickness_unique_id=occupational_sickness_unique_id,
            accrued_payment_adjustment=accrued_payment_adjustment,
            accrued_hours_adjustment=accrued_hours_adjustment,
            holiday_accrual_basis=holiday_accrual_basis,
            holiday_accrual_default_rate_type=holiday_accrual_default_rate_type,
            aggregated_service_date=aggregated_service_date,
            use_aggregated_service_date=use_aggregated_service_date,
            accrue_pay_code_set_unique_id=accrue_pay_code_set_unique_id,
            maximum_accrue_period=maximum_accrue_period,
        )

        return contract_leave_settings_response

