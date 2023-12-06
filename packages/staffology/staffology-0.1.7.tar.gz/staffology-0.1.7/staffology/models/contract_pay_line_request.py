import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.contract_payline_analysis_categories_codes import ContractPaylineAnalysisCategoriesCodes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPayLineRequest")

@attr.s(auto_attribs=True)
class ContractPayLineRequest:
    """
    Attributes:
        analysis_category_codes_json (Union[Unset, None, str]): Analysis category id and analysiscategoryCode json
        value (Union[Unset, float]): The amount to add or deduct (whether it is a deduction or addition depends on the
            PayCode used).
            If the PayCode has a CalculationType other than FixedAmount then this field will be a percentage.
            If the PayCode has a MultiplierType other than None then this field will be readonly and automatically
            calculated.
        rate (Union[Unset, None, float]): If the related  PayCode has a MultiplierType other than None then this field
            will be used as the rate per day or hour. Otherwise it isn't used
        multiplier (Union[Unset, None, float]): If the related PayCode has a MultiplierType other than None then this
            field will be used as number of days or hours
        description (Union[Unset, None, str]): A freeform description to accompany this line. It will be displayed on
            the payslip.
        code (Union[Unset, None, str]): The Code of the PayCode this line is assigned to. The PayCode determines the
            treatment of this line when it comes to NI, Tax and Pensions as well as whether it's a deduction or addition.
        tags (Union[Unset, None, List[str]]):
        child_id (Union[Unset, None, str]):
        is_net_to_gross (Union[Unset, bool]): If the PayLine is a fixed ammount addition without multiplier then this
            property may be set to true so that the amount of the addition to be considered a take home pay target.
        target_net_to_gross_value (Union[Unset, None, float]): The orginal net fixed addition amount that is considered
            to be a take home pay target.
        net_to_gross_discrepancy (Union[Unset, None, float]): The discrepancy between the targeted and the calculated
            grossed up value durig a net to gross calculation.
        effective_from (Union[Unset, None, datetime.date]): The date the payline starts being calculated in payrun
        effective_to (Union[Unset, None, datetime.date]): The date the payline stops being calculated in payrun
        is_auto_generated_basic_pay_line (Union[Unset, bool]):
        percentage_of_effective_days (Union[Unset, None, float]): The percentage of working days the effective dates
            span for pro-rata'ing values, calculated/set during each payrun
        total_working_days (Union[Unset, None, float]):
        auto_adjust_for_leave (Union[Unset, bool]): Automatically reduce the PayAmount when the Employee has Leave that
            is either Not Paid or has Statutory Pay.
            If set to false then you must manually reduce their payment to reflect any Leave
        is_automatic_back_pay (Union[Unset, bool]): Automatically calculate backpay and add or modify the necessary pay
            lines for this addition/deduction when a pay run is created.
            Applicable only to employee level addition/deduction pay lines.
            If set to false then you must manually handle the calculation and adding of backpay lines.
        ignore_initial_back_pay (Union[Unset, bool]): Skip the automatic backpay calculation on the first pay run, if
            the addition/deduction had been paid outside or Staffology.
            If set to false, the automatic backpay calculation will be performed on the first pay run.
        contributes_to_basic_pay (Union[Unset, bool]): Indicates whether this PayLine contributes to the basic pay of
            the Employee.
        total_paid_days (Union[Unset, None, float]):
        role_id (Union[Unset, None, str]): The employee role which is associated with this pay line.
            If set to null, the pay line is not related with a role.
        earned_from (Union[Unset, None, datetime.date]):
        earned_to (Union[Unset, None, datetime.date]):
        annual_value (Union[Unset, None, float]): The original value from the PayLine before we modify it
            Currently only used when CalculationType is set to FixedAnnualAmount
            so we can determine whether the payline value needs calculating or not
            To recalculate set to null with annual amount recorded in Value
        department (Union[Unset, None, str]): Department code which we want to override in payline
        cost_centre (Union[Unset, None, str]): CostCentre code which we want to override in payline
        department_id (Union[Unset, None, str]): Department uniqueId which we want to override in payline
        cost_centre_id (Union[Unset, None, str]): CostCentre uniqueId which we want to override in payline
        analysis_categories_codes (Union[Unset, None, List[ContractPaylineAnalysisCategoriesCodes]]): List of
            analysiscategory id and analysiscategoryCode id
        analysis_category_code_ids (Union[Unset, None, List[str]]): Array of analysiscategoryCode uniqueId
    """

    analysis_category_codes_json: Union[Unset, None, str] = UNSET
    value: Union[Unset, float] = UNSET
    rate: Union[Unset, None, float] = UNSET
    multiplier: Union[Unset, None, float] = UNSET
    description: Union[Unset, None, str] = UNSET
    code: Union[Unset, None, str] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    child_id: Union[Unset, None, str] = UNSET
    is_net_to_gross: Union[Unset, bool] = UNSET
    target_net_to_gross_value: Union[Unset, None, float] = UNSET
    net_to_gross_discrepancy: Union[Unset, None, float] = UNSET
    effective_from: Union[Unset, None, datetime.date] = UNSET
    effective_to: Union[Unset, None, datetime.date] = UNSET
    is_auto_generated_basic_pay_line: Union[Unset, bool] = UNSET
    percentage_of_effective_days: Union[Unset, None, float] = UNSET
    total_working_days: Union[Unset, None, float] = UNSET
    auto_adjust_for_leave: Union[Unset, bool] = UNSET
    is_automatic_back_pay: Union[Unset, bool] = UNSET
    ignore_initial_back_pay: Union[Unset, bool] = UNSET
    contributes_to_basic_pay: Union[Unset, bool] = UNSET
    total_paid_days: Union[Unset, None, float] = UNSET
    role_id: Union[Unset, None, str] = UNSET
    earned_from: Union[Unset, None, datetime.date] = UNSET
    earned_to: Union[Unset, None, datetime.date] = UNSET
    annual_value: Union[Unset, None, float] = UNSET
    department: Union[Unset, None, str] = UNSET
    cost_centre: Union[Unset, None, str] = UNSET
    department_id: Union[Unset, None, str] = UNSET
    cost_centre_id: Union[Unset, None, str] = UNSET
    analysis_categories_codes: Union[Unset, None, List[ContractPaylineAnalysisCategoriesCodes]] = UNSET
    analysis_category_code_ids: Union[Unset, None, List[str]] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        analysis_category_codes_json = self.analysis_category_codes_json
        value = self.value
        rate = self.rate
        multiplier = self.multiplier
        description = self.description
        code = self.code
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags




        child_id = self.child_id
        is_net_to_gross = self.is_net_to_gross
        target_net_to_gross_value = self.target_net_to_gross_value
        net_to_gross_discrepancy = self.net_to_gross_discrepancy
        effective_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.effective_from, Unset):
            effective_from = self.effective_from.isoformat() if self.effective_from else None

        effective_to: Union[Unset, None, str] = UNSET
        if not isinstance(self.effective_to, Unset):
            effective_to = self.effective_to.isoformat() if self.effective_to else None

        is_auto_generated_basic_pay_line = self.is_auto_generated_basic_pay_line
        percentage_of_effective_days = self.percentage_of_effective_days
        total_working_days = self.total_working_days
        auto_adjust_for_leave = self.auto_adjust_for_leave
        is_automatic_back_pay = self.is_automatic_back_pay
        ignore_initial_back_pay = self.ignore_initial_back_pay
        contributes_to_basic_pay = self.contributes_to_basic_pay
        total_paid_days = self.total_paid_days
        role_id = self.role_id
        earned_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.earned_from, Unset):
            earned_from = self.earned_from.isoformat() if self.earned_from else None

        earned_to: Union[Unset, None, str] = UNSET
        if not isinstance(self.earned_to, Unset):
            earned_to = self.earned_to.isoformat() if self.earned_to else None

        annual_value = self.annual_value
        department = self.department
        cost_centre = self.cost_centre
        department_id = self.department_id
        cost_centre_id = self.cost_centre_id
        analysis_categories_codes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.analysis_categories_codes, Unset):
            if self.analysis_categories_codes is None:
                analysis_categories_codes = None
            else:
                analysis_categories_codes = []
                for analysis_categories_codes_item_data in self.analysis_categories_codes:
                    analysis_categories_codes_item = analysis_categories_codes_item_data.to_dict()

                    analysis_categories_codes.append(analysis_categories_codes_item)




        analysis_category_code_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.analysis_category_code_ids, Unset):
            if self.analysis_category_code_ids is None:
                analysis_category_code_ids = None
            else:
                analysis_category_code_ids = self.analysis_category_code_ids





        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if analysis_category_codes_json is not UNSET:
            field_dict["analysisCategoryCodesJson"] = analysis_category_codes_json
        if value is not UNSET:
            field_dict["value"] = value
        if rate is not UNSET:
            field_dict["rate"] = rate
        if multiplier is not UNSET:
            field_dict["multiplier"] = multiplier
        if description is not UNSET:
            field_dict["description"] = description
        if code is not UNSET:
            field_dict["code"] = code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if child_id is not UNSET:
            field_dict["childId"] = child_id
        if is_net_to_gross is not UNSET:
            field_dict["isNetToGross"] = is_net_to_gross
        if target_net_to_gross_value is not UNSET:
            field_dict["targetNetToGrossValue"] = target_net_to_gross_value
        if net_to_gross_discrepancy is not UNSET:
            field_dict["netToGrossDiscrepancy"] = net_to_gross_discrepancy
        if effective_from is not UNSET:
            field_dict["effectiveFrom"] = effective_from
        if effective_to is not UNSET:
            field_dict["effectiveTo"] = effective_to
        if is_auto_generated_basic_pay_line is not UNSET:
            field_dict["isAutoGeneratedBasicPayLine"] = is_auto_generated_basic_pay_line
        if percentage_of_effective_days is not UNSET:
            field_dict["percentageOfEffectiveDays"] = percentage_of_effective_days
        if total_working_days is not UNSET:
            field_dict["totalWorkingDays"] = total_working_days
        if auto_adjust_for_leave is not UNSET:
            field_dict["autoAdjustForLeave"] = auto_adjust_for_leave
        if is_automatic_back_pay is not UNSET:
            field_dict["isAutomaticBackPay"] = is_automatic_back_pay
        if ignore_initial_back_pay is not UNSET:
            field_dict["ignoreInitialBackPay"] = ignore_initial_back_pay
        if contributes_to_basic_pay is not UNSET:
            field_dict["contributesToBasicPay"] = contributes_to_basic_pay
        if total_paid_days is not UNSET:
            field_dict["totalPaidDays"] = total_paid_days
        if role_id is not UNSET:
            field_dict["roleId"] = role_id
        if earned_from is not UNSET:
            field_dict["earnedFrom"] = earned_from
        if earned_to is not UNSET:
            field_dict["earnedTo"] = earned_to
        if annual_value is not UNSET:
            field_dict["annualValue"] = annual_value
        if department is not UNSET:
            field_dict["department"] = department
        if cost_centre is not UNSET:
            field_dict["costCentre"] = cost_centre
        if department_id is not UNSET:
            field_dict["departmentId"] = department_id
        if cost_centre_id is not UNSET:
            field_dict["costCentreId"] = cost_centre_id
        if analysis_categories_codes is not UNSET:
            field_dict["analysisCategoriesCodes"] = analysis_categories_codes
        if analysis_category_code_ids is not UNSET:
            field_dict["analysisCategoryCodeIds"] = analysis_category_code_ids

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        analysis_category_codes_json = d.pop("analysisCategoryCodesJson", UNSET)

        value = d.pop("value", UNSET)

        rate = d.pop("rate", UNSET)

        multiplier = d.pop("multiplier", UNSET)

        description = d.pop("description", UNSET)

        code = d.pop("code", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))


        child_id = d.pop("childId", UNSET)

        is_net_to_gross = d.pop("isNetToGross", UNSET)

        target_net_to_gross_value = d.pop("targetNetToGrossValue", UNSET)

        net_to_gross_discrepancy = d.pop("netToGrossDiscrepancy", UNSET)

        _effective_from = d.pop("effectiveFrom", UNSET)
        effective_from: Union[Unset, None, datetime.date]
        if _effective_from is None:
            effective_from = None
        elif isinstance(_effective_from,  Unset):
            effective_from = UNSET
        else:
            effective_from = isoparse(_effective_from).date()




        _effective_to = d.pop("effectiveTo", UNSET)
        effective_to: Union[Unset, None, datetime.date]
        if _effective_to is None:
            effective_to = None
        elif isinstance(_effective_to,  Unset):
            effective_to = UNSET
        else:
            effective_to = isoparse(_effective_to).date()




        is_auto_generated_basic_pay_line = d.pop("isAutoGeneratedBasicPayLine", UNSET)

        percentage_of_effective_days = d.pop("percentageOfEffectiveDays", UNSET)

        total_working_days = d.pop("totalWorkingDays", UNSET)

        auto_adjust_for_leave = d.pop("autoAdjustForLeave", UNSET)

        is_automatic_back_pay = d.pop("isAutomaticBackPay", UNSET)

        ignore_initial_back_pay = d.pop("ignoreInitialBackPay", UNSET)

        contributes_to_basic_pay = d.pop("contributesToBasicPay", UNSET)

        total_paid_days = d.pop("totalPaidDays", UNSET)

        role_id = d.pop("roleId", UNSET)

        _earned_from = d.pop("earnedFrom", UNSET)
        earned_from: Union[Unset, None, datetime.date]
        if _earned_from is None:
            earned_from = None
        elif isinstance(_earned_from,  Unset):
            earned_from = UNSET
        else:
            earned_from = isoparse(_earned_from).date()




        _earned_to = d.pop("earnedTo", UNSET)
        earned_to: Union[Unset, None, datetime.date]
        if _earned_to is None:
            earned_to = None
        elif isinstance(_earned_to,  Unset):
            earned_to = UNSET
        else:
            earned_to = isoparse(_earned_to).date()




        annual_value = d.pop("annualValue", UNSET)

        department = d.pop("department", UNSET)

        cost_centre = d.pop("costCentre", UNSET)

        department_id = d.pop("departmentId", UNSET)

        cost_centre_id = d.pop("costCentreId", UNSET)

        analysis_categories_codes = []
        _analysis_categories_codes = d.pop("analysisCategoriesCodes", UNSET)
        for analysis_categories_codes_item_data in (_analysis_categories_codes or []):
            analysis_categories_codes_item = ContractPaylineAnalysisCategoriesCodes.from_dict(analysis_categories_codes_item_data)



            analysis_categories_codes.append(analysis_categories_codes_item)


        analysis_category_code_ids = cast(List[str], d.pop("analysisCategoryCodeIds", UNSET))


        contract_pay_line_request = cls(
            analysis_category_codes_json=analysis_category_codes_json,
            value=value,
            rate=rate,
            multiplier=multiplier,
            description=description,
            code=code,
            tags=tags,
            child_id=child_id,
            is_net_to_gross=is_net_to_gross,
            target_net_to_gross_value=target_net_to_gross_value,
            net_to_gross_discrepancy=net_to_gross_discrepancy,
            effective_from=effective_from,
            effective_to=effective_to,
            is_auto_generated_basic_pay_line=is_auto_generated_basic_pay_line,
            percentage_of_effective_days=percentage_of_effective_days,
            total_working_days=total_working_days,
            auto_adjust_for_leave=auto_adjust_for_leave,
            is_automatic_back_pay=is_automatic_back_pay,
            ignore_initial_back_pay=ignore_initial_back_pay,
            contributes_to_basic_pay=contributes_to_basic_pay,
            total_paid_days=total_paid_days,
            role_id=role_id,
            earned_from=earned_from,
            earned_to=earned_to,
            annual_value=annual_value,
            department=department,
            cost_centre=cost_centre,
            department_id=department_id,
            cost_centre_id=cost_centre_id,
            analysis_categories_codes=analysis_categories_codes,
            analysis_category_code_ids=analysis_category_code_ids,
        )

        return contract_pay_line_request

