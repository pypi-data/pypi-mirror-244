import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.item import Item
from ..models.leave_assumed_pensionable_pay import LeaveAssumedPensionablePay
from ..models.leave_calculation_type import LeaveCalculationType
from ..models.leave_pay_type import LeavePayType
from ..models.leave_type import LeaveType
from ..models.linked_piw import LinkedPiw
from ..models.stat_pay_frequency import StatPayFrequency
from ..types import UNSET, Unset

T = TypeVar("T", bound="Leave")

@attr.s(auto_attribs=True)
class Leave:
    """Used to represent Leave, including Holiday and Statutory leave (such as Maternity Leave)

    Attributes:
        provider_id (Union[Unset, ExternalDataProviderId]):
        external_id (Union[Unset, None, str]): If the Leave comes from an ExternalDataProvider, then this is its Id in
            the ExternalDataProvider
        type (Union[Unset, LeaveType]):
        pay (Union[Unset, LeavePayType]):
        pay_frequency (Union[Unset, StatPayFrequency]):
        pay_run_exists_with_stat_pay (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]): The first day of Leave.
            If it's a half day PM then set the time portion to 12:00:00, otherwise leave it blank or set it to 00:00:00
        to (Union[Unset, datetime.datetime]): The last day of Leave.
            If it's a half day AM then set the time portion to 11:59:59, otherwise set it to 23:59:59
        notes (Union[Unset, None, str]): A free-form text field to record any comments
        average_weekly_earnings (Union[Unset, float]): The employees average weekly earnings. Only relevant for
            Statutory Pay
            It's advised that you don't try to calculate this yourself.
        automatic_awe_calculation (Union[Unset, bool]): If set to True then we'll automatically calculate the
            AverageWeeklyEarnings.
            Set it to false if you want to manually provide a figure that overrides our calculations
        baby_date (Union[Unset, None, datetime.date]): Only required for Parental Leave with Statutory Pay
            If Type is Maternity or Paternity then this is the date the baby is due.
            For Adoption this is the Matching Date.
        secondary_baby_date (Union[Unset, None, datetime.date]): Only used for Parental Leave with Statutory Pay
            If Type is Maternity, Paternity, SharedParental (Birth) then this is the the Baby Born Date.
            For Adoption or SharedParental (Adoption) this is the Expected Placement Date.
        tertiary_baby_date (Union[Unset, None, datetime.date]): Only used for Parental Leave with Statutory Pay
            If Type is Adoption this is the Placement Date.
        override_payment_description (Union[Unset, bool]): If Pay is StatutoryPay and you want to override our
            description that goes with the payment then set this to true
        overriden_payment_description (Union[Unset, None, str]): If OverridePaymentDescription is true and Pay is set to
            StatutoryPay then we'll use this as the description for the payment amount.
        working_days (Union[Unset, float]): [readonly] The number of working days covered by this leave.
            This is calculated based on the employees Working Pattern.
        working_days_override (Union[Unset, None, float]): If a value is provided here then this will be used in place
            of the calculated WorkingDays value
        total_days (Union[Unset, float]): [readonly] The number of days covered by this leave, regardless of whether or
            not they're working days.
            This is calculated based on the employees Working Pattern.
        total_days_override (Union[Unset, None, float]): If a value is provided here then this will be used in place of
            the calculated TotalDays value
        use_assumed_pensionable_pay (Union[Unset, bool]): If this Leave has Statutory Pay then if this is set to True
            we will use the value set in AssumedPensionablePay to work out the employer pension contributions
        assumed_pensionable_pays (Union[Unset, None, List[LeaveAssumedPensionablePay]]): if UseAssumedPensionablePay is
            True, then this is the value used to calculate the employer pension contributions
        offset_pay (Union[Unset, bool]): If this Leave has Statutory Pay  and this is set to True and the employe eis
            paid a fixed amoutn per period
            with Leave Adjustments set to automatic, then we'll reduce their pay for the period by the statutory amount
            so the employee still gets paid the full amount.
        ssp_pay_from_day_one (Union[Unset, bool]): If this is Sick Leave with Statutory Pay then setting this to true
            will force SSP to be paid from day one rather than the usual rule
            of the first Working Day after 3 Qualifying Days
        linked_piw (Union[Unset, LinkedPiw]): Linked Period of Incapacity for Work.
            If you record Sick Leave and select Statutory Pay then any other Sick Leave with Statutory Pay
            lasting 4 or more days in the previous 8 weeks will be linked to it
        kit_split_days (Union[Unset, None, List[datetime.datetime]]): If the LeaveType supports KIT/SPLIT days then use
            this property to store the list of dates
        historic_ssp_requires_processing (Union[Unset, bool]): Only used during the creation of historical SSP.
            When creating historical SSP, this will determine whether to pay that leave in the next PayRun.
        historic_sxp_requires_processing (Union[Unset, bool]): Used during to determine whether to back pay before
            current payrun
        opening_pay (Union[Unset, None, float]): Opening pay which has already been paid to the employee in another
            system
        use_opening_pay (Union[Unset, bool]): Use the OpeningPay which has already been paid in another system
        occupational_policy_id (Union[Unset, None, int]): Occupational Policy when leave type is sickness and payment
            type is occupational policy
        historic_osp_requires_processing (Union[Unset, bool]): Only used during the creation of sickness Occupational
            Policy.
            When creating historical SOP, this will determine whether to pay that leave in the next PayRun.
        occupational_maternity_policy_unique_id (Union[Unset, None, str]): Occupational Maternity Policy Id when leave
            type is Maternity and payment type is occupational policy
        opening_omp_pay (Union[Unset, None, float]): Opening occupational pay which has already been paid to the
            employee
        pay_run_exists_with_occ_pay (Union[Unset, bool]):
        calculation_type (Union[Unset, LeaveCalculationType]):
        strike_hours_to_deduct (Union[Unset, None, float]): The number of hours to be deducted at the employee's
            contractual rate
            This property is valid for strike deducted hours
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    provider_id: Union[Unset, ExternalDataProviderId] = UNSET
    external_id: Union[Unset, None, str] = UNSET
    type: Union[Unset, LeaveType] = UNSET
    pay: Union[Unset, LeavePayType] = UNSET
    pay_frequency: Union[Unset, StatPayFrequency] = UNSET
    pay_run_exists_with_stat_pay: Union[Unset, bool] = UNSET
    from_: Union[Unset, datetime.datetime] = UNSET
    to: Union[Unset, datetime.datetime] = UNSET
    notes: Union[Unset, None, str] = UNSET
    average_weekly_earnings: Union[Unset, float] = UNSET
    automatic_awe_calculation: Union[Unset, bool] = UNSET
    baby_date: Union[Unset, None, datetime.date] = UNSET
    secondary_baby_date: Union[Unset, None, datetime.date] = UNSET
    tertiary_baby_date: Union[Unset, None, datetime.date] = UNSET
    override_payment_description: Union[Unset, bool] = UNSET
    overriden_payment_description: Union[Unset, None, str] = UNSET
    working_days: Union[Unset, float] = UNSET
    working_days_override: Union[Unset, None, float] = UNSET
    total_days: Union[Unset, float] = UNSET
    total_days_override: Union[Unset, None, float] = UNSET
    use_assumed_pensionable_pay: Union[Unset, bool] = UNSET
    assumed_pensionable_pays: Union[Unset, None, List[LeaveAssumedPensionablePay]] = UNSET
    offset_pay: Union[Unset, bool] = UNSET
    ssp_pay_from_day_one: Union[Unset, bool] = UNSET
    linked_piw: Union[Unset, LinkedPiw] = UNSET
    kit_split_days: Union[Unset, None, List[datetime.datetime]] = UNSET
    historic_ssp_requires_processing: Union[Unset, bool] = UNSET
    historic_sxp_requires_processing: Union[Unset, bool] = UNSET
    opening_pay: Union[Unset, None, float] = UNSET
    use_opening_pay: Union[Unset, bool] = UNSET
    occupational_policy_id: Union[Unset, None, int] = UNSET
    historic_osp_requires_processing: Union[Unset, bool] = UNSET
    occupational_maternity_policy_unique_id: Union[Unset, None, str] = UNSET
    opening_omp_pay: Union[Unset, None, float] = UNSET
    pay_run_exists_with_occ_pay: Union[Unset, bool] = UNSET
    calculation_type: Union[Unset, LeaveCalculationType] = UNSET
    strike_hours_to_deduct: Union[Unset, None, float] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        provider_id: Union[Unset, str] = UNSET
        if not isinstance(self.provider_id, Unset):
            provider_id = self.provider_id.value

        external_id = self.external_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        pay: Union[Unset, str] = UNSET
        if not isinstance(self.pay, Unset):
            pay = self.pay.value

        pay_frequency: Union[Unset, str] = UNSET
        if not isinstance(self.pay_frequency, Unset):
            pay_frequency = self.pay_frequency.value

        pay_run_exists_with_stat_pay = self.pay_run_exists_with_stat_pay
        from_: Union[Unset, str] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.isoformat()

        to: Union[Unset, str] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.isoformat()

        notes = self.notes
        average_weekly_earnings = self.average_weekly_earnings
        automatic_awe_calculation = self.automatic_awe_calculation
        baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.baby_date, Unset):
            baby_date = self.baby_date.isoformat() if self.baby_date else None

        secondary_baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.secondary_baby_date, Unset):
            secondary_baby_date = self.secondary_baby_date.isoformat() if self.secondary_baby_date else None

        tertiary_baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.tertiary_baby_date, Unset):
            tertiary_baby_date = self.tertiary_baby_date.isoformat() if self.tertiary_baby_date else None

        override_payment_description = self.override_payment_description
        overriden_payment_description = self.overriden_payment_description
        working_days = self.working_days
        working_days_override = self.working_days_override
        total_days = self.total_days
        total_days_override = self.total_days_override
        use_assumed_pensionable_pay = self.use_assumed_pensionable_pay
        assumed_pensionable_pays: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.assumed_pensionable_pays, Unset):
            if self.assumed_pensionable_pays is None:
                assumed_pensionable_pays = None
            else:
                assumed_pensionable_pays = []
                for assumed_pensionable_pays_item_data in self.assumed_pensionable_pays:
                    assumed_pensionable_pays_item = assumed_pensionable_pays_item_data.to_dict()

                    assumed_pensionable_pays.append(assumed_pensionable_pays_item)




        offset_pay = self.offset_pay
        ssp_pay_from_day_one = self.ssp_pay_from_day_one
        linked_piw: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.linked_piw, Unset):
            linked_piw = self.linked_piw.to_dict()

        kit_split_days: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.kit_split_days, Unset):
            if self.kit_split_days is None:
                kit_split_days = None
            else:
                kit_split_days = []
                for kit_split_days_item_data in self.kit_split_days:
                    kit_split_days_item = kit_split_days_item_data.isoformat()

                    kit_split_days.append(kit_split_days_item)




        historic_ssp_requires_processing = self.historic_ssp_requires_processing
        historic_sxp_requires_processing = self.historic_sxp_requires_processing
        opening_pay = self.opening_pay
        use_opening_pay = self.use_opening_pay
        occupational_policy_id = self.occupational_policy_id
        historic_osp_requires_processing = self.historic_osp_requires_processing
        occupational_maternity_policy_unique_id = self.occupational_maternity_policy_unique_id
        opening_omp_pay = self.opening_omp_pay
        pay_run_exists_with_occ_pay = self.pay_run_exists_with_occ_pay
        calculation_type: Union[Unset, str] = UNSET
        if not isinstance(self.calculation_type, Unset):
            calculation_type = self.calculation_type.value

        strike_hours_to_deduct = self.strike_hours_to_deduct
        document_count = self.document_count
        documents: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            if self.documents is None:
                documents = None
            else:
                documents = []
                for documents_item_data in self.documents:
                    documents_item = documents_item_data.to_dict()

                    documents.append(documents_item)




        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if provider_id is not UNSET:
            field_dict["providerId"] = provider_id
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if type is not UNSET:
            field_dict["type"] = type
        if pay is not UNSET:
            field_dict["pay"] = pay
        if pay_frequency is not UNSET:
            field_dict["payFrequency"] = pay_frequency
        if pay_run_exists_with_stat_pay is not UNSET:
            field_dict["payRunExistsWithStatPay"] = pay_run_exists_with_stat_pay
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if notes is not UNSET:
            field_dict["notes"] = notes
        if average_weekly_earnings is not UNSET:
            field_dict["averageWeeklyEarnings"] = average_weekly_earnings
        if automatic_awe_calculation is not UNSET:
            field_dict["automaticAWECalculation"] = automatic_awe_calculation
        if baby_date is not UNSET:
            field_dict["babyDate"] = baby_date
        if secondary_baby_date is not UNSET:
            field_dict["secondaryBabyDate"] = secondary_baby_date
        if tertiary_baby_date is not UNSET:
            field_dict["tertiaryBabyDate"] = tertiary_baby_date
        if override_payment_description is not UNSET:
            field_dict["overridePaymentDescription"] = override_payment_description
        if overriden_payment_description is not UNSET:
            field_dict["overridenPaymentDescription"] = overriden_payment_description
        if working_days is not UNSET:
            field_dict["workingDays"] = working_days
        if working_days_override is not UNSET:
            field_dict["workingDaysOverride"] = working_days_override
        if total_days is not UNSET:
            field_dict["totalDays"] = total_days
        if total_days_override is not UNSET:
            field_dict["totalDaysOverride"] = total_days_override
        if use_assumed_pensionable_pay is not UNSET:
            field_dict["useAssumedPensionablePay"] = use_assumed_pensionable_pay
        if assumed_pensionable_pays is not UNSET:
            field_dict["assumedPensionablePays"] = assumed_pensionable_pays
        if offset_pay is not UNSET:
            field_dict["offsetPay"] = offset_pay
        if ssp_pay_from_day_one is not UNSET:
            field_dict["sspPayFromDayOne"] = ssp_pay_from_day_one
        if linked_piw is not UNSET:
            field_dict["linkedPiw"] = linked_piw
        if kit_split_days is not UNSET:
            field_dict["kitSplitDays"] = kit_split_days
        if historic_ssp_requires_processing is not UNSET:
            field_dict["historicSspRequiresProcessing"] = historic_ssp_requires_processing
        if historic_sxp_requires_processing is not UNSET:
            field_dict["historicSxpRequiresProcessing"] = historic_sxp_requires_processing
        if opening_pay is not UNSET:
            field_dict["openingPay"] = opening_pay
        if use_opening_pay is not UNSET:
            field_dict["useOpeningPay"] = use_opening_pay
        if occupational_policy_id is not UNSET:
            field_dict["occupationalPolicyId"] = occupational_policy_id
        if historic_osp_requires_processing is not UNSET:
            field_dict["historicOspRequiresProcessing"] = historic_osp_requires_processing
        if occupational_maternity_policy_unique_id is not UNSET:
            field_dict["occupationalMaternityPolicyUniqueId"] = occupational_maternity_policy_unique_id
        if opening_omp_pay is not UNSET:
            field_dict["openingOmpPay"] = opening_omp_pay
        if pay_run_exists_with_occ_pay is not UNSET:
            field_dict["payRunExistsWithOccPay"] = pay_run_exists_with_occ_pay
        if calculation_type is not UNSET:
            field_dict["calculationType"] = calculation_type
        if strike_hours_to_deduct is not UNSET:
            field_dict["strikeHoursToDeduct"] = strike_hours_to_deduct
        if document_count is not UNSET:
            field_dict["documentCount"] = document_count
        if documents is not UNSET:
            field_dict["documents"] = documents
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _provider_id = d.pop("providerId", UNSET)
        provider_id: Union[Unset, ExternalDataProviderId]
        if isinstance(_provider_id,  Unset):
            provider_id = UNSET
        else:
            provider_id = ExternalDataProviderId(_provider_id)




        external_id = d.pop("externalId", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LeaveType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = LeaveType(_type)




        _pay = d.pop("pay", UNSET)
        pay: Union[Unset, LeavePayType]
        if isinstance(_pay,  Unset):
            pay = UNSET
        else:
            pay = LeavePayType(_pay)




        _pay_frequency = d.pop("payFrequency", UNSET)
        pay_frequency: Union[Unset, StatPayFrequency]
        if isinstance(_pay_frequency,  Unset):
            pay_frequency = UNSET
        else:
            pay_frequency = StatPayFrequency(_pay_frequency)




        pay_run_exists_with_stat_pay = d.pop("payRunExistsWithStatPay", UNSET)

        _from_ = d.pop("from", UNSET)
        from_: Union[Unset, datetime.datetime]
        if isinstance(_from_,  Unset):
            from_ = UNSET
        else:
            from_ = isoparse(_from_)




        _to = d.pop("to", UNSET)
        to: Union[Unset, datetime.datetime]
        if isinstance(_to,  Unset):
            to = UNSET
        else:
            to = isoparse(_to)




        notes = d.pop("notes", UNSET)

        average_weekly_earnings = d.pop("averageWeeklyEarnings", UNSET)

        automatic_awe_calculation = d.pop("automaticAWECalculation", UNSET)

        _baby_date = d.pop("babyDate", UNSET)
        baby_date: Union[Unset, None, datetime.date]
        if _baby_date is None:
            baby_date = None
        elif isinstance(_baby_date,  Unset):
            baby_date = UNSET
        else:
            baby_date = isoparse(_baby_date).date()




        _secondary_baby_date = d.pop("secondaryBabyDate", UNSET)
        secondary_baby_date: Union[Unset, None, datetime.date]
        if _secondary_baby_date is None:
            secondary_baby_date = None
        elif isinstance(_secondary_baby_date,  Unset):
            secondary_baby_date = UNSET
        else:
            secondary_baby_date = isoparse(_secondary_baby_date).date()




        _tertiary_baby_date = d.pop("tertiaryBabyDate", UNSET)
        tertiary_baby_date: Union[Unset, None, datetime.date]
        if _tertiary_baby_date is None:
            tertiary_baby_date = None
        elif isinstance(_tertiary_baby_date,  Unset):
            tertiary_baby_date = UNSET
        else:
            tertiary_baby_date = isoparse(_tertiary_baby_date).date()




        override_payment_description = d.pop("overridePaymentDescription", UNSET)

        overriden_payment_description = d.pop("overridenPaymentDescription", UNSET)

        working_days = d.pop("workingDays", UNSET)

        working_days_override = d.pop("workingDaysOverride", UNSET)

        total_days = d.pop("totalDays", UNSET)

        total_days_override = d.pop("totalDaysOverride", UNSET)

        use_assumed_pensionable_pay = d.pop("useAssumedPensionablePay", UNSET)

        assumed_pensionable_pays = []
        _assumed_pensionable_pays = d.pop("assumedPensionablePays", UNSET)
        for assumed_pensionable_pays_item_data in (_assumed_pensionable_pays or []):
            assumed_pensionable_pays_item = LeaveAssumedPensionablePay.from_dict(assumed_pensionable_pays_item_data)



            assumed_pensionable_pays.append(assumed_pensionable_pays_item)


        offset_pay = d.pop("offsetPay", UNSET)

        ssp_pay_from_day_one = d.pop("sspPayFromDayOne", UNSET)

        _linked_piw = d.pop("linkedPiw", UNSET)
        linked_piw: Union[Unset, LinkedPiw]
        if isinstance(_linked_piw,  Unset):
            linked_piw = UNSET
        else:
            linked_piw = LinkedPiw.from_dict(_linked_piw)




        kit_split_days = []
        _kit_split_days = d.pop("kitSplitDays", UNSET)
        for kit_split_days_item_data in (_kit_split_days or []):
            kit_split_days_item = isoparse(kit_split_days_item_data)



            kit_split_days.append(kit_split_days_item)


        historic_ssp_requires_processing = d.pop("historicSspRequiresProcessing", UNSET)

        historic_sxp_requires_processing = d.pop("historicSxpRequiresProcessing", UNSET)

        opening_pay = d.pop("openingPay", UNSET)

        use_opening_pay = d.pop("useOpeningPay", UNSET)

        occupational_policy_id = d.pop("occupationalPolicyId", UNSET)

        historic_osp_requires_processing = d.pop("historicOspRequiresProcessing", UNSET)

        occupational_maternity_policy_unique_id = d.pop("occupationalMaternityPolicyUniqueId", UNSET)

        opening_omp_pay = d.pop("openingOmpPay", UNSET)

        pay_run_exists_with_occ_pay = d.pop("payRunExistsWithOccPay", UNSET)

        _calculation_type = d.pop("calculationType", UNSET)
        calculation_type: Union[Unset, LeaveCalculationType]
        if isinstance(_calculation_type,  Unset):
            calculation_type = UNSET
        else:
            calculation_type = LeaveCalculationType(_calculation_type)




        strike_hours_to_deduct = d.pop("strikeHoursToDeduct", UNSET)

        document_count = d.pop("documentCount", UNSET)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in (_documents or []):
            documents_item = Item.from_dict(documents_item_data)



            documents.append(documents_item)


        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        id = d.pop("id", UNSET)

        leave = cls(
            provider_id=provider_id,
            external_id=external_id,
            type=type,
            pay=pay,
            pay_frequency=pay_frequency,
            pay_run_exists_with_stat_pay=pay_run_exists_with_stat_pay,
            from_=from_,
            to=to,
            notes=notes,
            average_weekly_earnings=average_weekly_earnings,
            automatic_awe_calculation=automatic_awe_calculation,
            baby_date=baby_date,
            secondary_baby_date=secondary_baby_date,
            tertiary_baby_date=tertiary_baby_date,
            override_payment_description=override_payment_description,
            overriden_payment_description=overriden_payment_description,
            working_days=working_days,
            working_days_override=working_days_override,
            total_days=total_days,
            total_days_override=total_days_override,
            use_assumed_pensionable_pay=use_assumed_pensionable_pay,
            assumed_pensionable_pays=assumed_pensionable_pays,
            offset_pay=offset_pay,
            ssp_pay_from_day_one=ssp_pay_from_day_one,
            linked_piw=linked_piw,
            kit_split_days=kit_split_days,
            historic_ssp_requires_processing=historic_ssp_requires_processing,
            historic_sxp_requires_processing=historic_sxp_requires_processing,
            opening_pay=opening_pay,
            use_opening_pay=use_opening_pay,
            occupational_policy_id=occupational_policy_id,
            historic_osp_requires_processing=historic_osp_requires_processing,
            occupational_maternity_policy_unique_id=occupational_maternity_policy_unique_id,
            opening_omp_pay=opening_omp_pay,
            pay_run_exists_with_occ_pay=pay_run_exists_with_occ_pay,
            calculation_type=calculation_type,
            strike_hours_to_deduct=strike_hours_to_deduct,
            document_count=document_count,
            documents=documents,
            employee=employee,
            id=id,
        )

        return leave

