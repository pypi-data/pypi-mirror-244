from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calendar_month import CalendarMonth
from ..models.occupational_policy_entitlement import OccupationalPolicyEntitlement
from ..models.occupational_policy_pay_calculated_on import OccupationalPolicyPayCalculatedOn
from ..models.occupational_policy_sickness_year import OccupationalPolicySicknessYear
from ..models.occupational_policy_type import OccupationalPolicyType
from ..models.service_band import ServiceBand
from ..types import UNSET, Unset

T = TypeVar("T", bound="OccupationalPolicy")

@attr.s(auto_attribs=True)
class OccupationalPolicy:
    """
    Attributes:
        policy_name (str): The unique policy name
        type (OccupationalPolicyType):
        entitlement (OccupationalPolicyEntitlement):
        sickness_year (OccupationalPolicySicknessYear):
        policy_start_month (Union[Unset, CalendarMonth]):
        service_bands (Union[Unset, None, List[ServiceBand]]): Service Bands Json
        pay_calculated_on (Union[Unset, OccupationalPolicyPayCalculatedOn]):
        pay_code_set_unique_id (Union[Unset, None, str]):
        use_aggregated_service_date (Union[Unset, bool]):
    """

    policy_name: str
    type: OccupationalPolicyType
    entitlement: OccupationalPolicyEntitlement
    sickness_year: OccupationalPolicySicknessYear
    policy_start_month: Union[Unset, CalendarMonth] = UNSET
    service_bands: Union[Unset, None, List[ServiceBand]] = UNSET
    pay_calculated_on: Union[Unset, OccupationalPolicyPayCalculatedOn] = UNSET
    pay_code_set_unique_id: Union[Unset, None, str] = UNSET
    use_aggregated_service_date: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        policy_name = self.policy_name
        type = self.type.value

        entitlement = self.entitlement.value

        sickness_year = self.sickness_year.value

        policy_start_month: Union[Unset, str] = UNSET
        if not isinstance(self.policy_start_month, Unset):
            policy_start_month = self.policy_start_month.value

        service_bands: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.service_bands, Unset):
            if self.service_bands is None:
                service_bands = None
            else:
                service_bands = []
                for service_bands_item_data in self.service_bands:
                    service_bands_item = service_bands_item_data.to_dict()

                    service_bands.append(service_bands_item)




        pay_calculated_on: Union[Unset, str] = UNSET
        if not isinstance(self.pay_calculated_on, Unset):
            pay_calculated_on = self.pay_calculated_on.value

        pay_code_set_unique_id = self.pay_code_set_unique_id
        use_aggregated_service_date = self.use_aggregated_service_date

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "policyName": policy_name,
            "type": type,
            "entitlement": entitlement,
            "sicknessYear": sickness_year,
        })
        if policy_start_month is not UNSET:
            field_dict["policyStartMonth"] = policy_start_month
        if service_bands is not UNSET:
            field_dict["serviceBands"] = service_bands
        if pay_calculated_on is not UNSET:
            field_dict["payCalculatedOn"] = pay_calculated_on
        if pay_code_set_unique_id is not UNSET:
            field_dict["payCodeSetUniqueId"] = pay_code_set_unique_id
        if use_aggregated_service_date is not UNSET:
            field_dict["useAggregatedServiceDate"] = use_aggregated_service_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        policy_name = d.pop("policyName")

        type = OccupationalPolicyType(d.pop("type"))




        entitlement = OccupationalPolicyEntitlement(d.pop("entitlement"))




        sickness_year = OccupationalPolicySicknessYear(d.pop("sicknessYear"))




        _policy_start_month = d.pop("policyStartMonth", UNSET)
        policy_start_month: Union[Unset, CalendarMonth]
        if isinstance(_policy_start_month,  Unset):
            policy_start_month = UNSET
        else:
            policy_start_month = CalendarMonth(_policy_start_month)




        service_bands = []
        _service_bands = d.pop("serviceBands", UNSET)
        for service_bands_item_data in (_service_bands or []):
            service_bands_item = ServiceBand.from_dict(service_bands_item_data)



            service_bands.append(service_bands_item)


        _pay_calculated_on = d.pop("payCalculatedOn", UNSET)
        pay_calculated_on: Union[Unset, OccupationalPolicyPayCalculatedOn]
        if isinstance(_pay_calculated_on,  Unset):
            pay_calculated_on = UNSET
        else:
            pay_calculated_on = OccupationalPolicyPayCalculatedOn(_pay_calculated_on)




        pay_code_set_unique_id = d.pop("payCodeSetUniqueId", UNSET)

        use_aggregated_service_date = d.pop("useAggregatedServiceDate", UNSET)

        occupational_policy = cls(
            policy_name=policy_name,
            type=type,
            entitlement=entitlement,
            sickness_year=sickness_year,
            policy_start_month=policy_start_month,
            service_bands=service_bands,
            pay_calculated_on=pay_calculated_on,
            pay_code_set_unique_id=pay_code_set_unique_id,
            use_aggregated_service_date=use_aggregated_service_date,
        )

        return occupational_policy

