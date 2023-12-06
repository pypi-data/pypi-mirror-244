from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantBillingSettings")

@attr.s(auto_attribs=True)
class TenantBillingSettings:
    """
    Attributes:
        discount (Union[Unset, float]):
        monthly_minimum (Union[Unset, float]):
        aggregated_pricing (Union[Unset, bool]):
        bill_to (Union[Unset, None, str]): If all activity for a Tenant is being biulled to a specifc user, set the
            email address here
        pricing_table (Union[Unset, None, str]): If BillTo is set, then specify a Pricing Table to use from the
            Staffology tenant, otherwise the default Staffology Pricing Table will be used
        net_suite_default_item_code (Union[Unset, None, str]): [readonly] The item code used in the NetSuite billing if
            not specified in the pricing table
        net_suite_default_description (Union[Unset, None, str]): [readonly] The product description used in the NetSuite
            billing if not specified in the pricing table
    """

    discount: Union[Unset, float] = UNSET
    monthly_minimum: Union[Unset, float] = UNSET
    aggregated_pricing: Union[Unset, bool] = UNSET
    bill_to: Union[Unset, None, str] = UNSET
    pricing_table: Union[Unset, None, str] = UNSET
    net_suite_default_item_code: Union[Unset, None, str] = UNSET
    net_suite_default_description: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        discount = self.discount
        monthly_minimum = self.monthly_minimum
        aggregated_pricing = self.aggregated_pricing
        bill_to = self.bill_to
        pricing_table = self.pricing_table
        net_suite_default_item_code = self.net_suite_default_item_code
        net_suite_default_description = self.net_suite_default_description

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if discount is not UNSET:
            field_dict["discount"] = discount
        if monthly_minimum is not UNSET:
            field_dict["monthlyMinimum"] = monthly_minimum
        if aggregated_pricing is not UNSET:
            field_dict["aggregatedPricing"] = aggregated_pricing
        if bill_to is not UNSET:
            field_dict["billTo"] = bill_to
        if pricing_table is not UNSET:
            field_dict["pricingTable"] = pricing_table
        if net_suite_default_item_code is not UNSET:
            field_dict["netSuiteDefaultItemCode"] = net_suite_default_item_code
        if net_suite_default_description is not UNSET:
            field_dict["netSuiteDefaultDescription"] = net_suite_default_description

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        discount = d.pop("discount", UNSET)

        monthly_minimum = d.pop("monthlyMinimum", UNSET)

        aggregated_pricing = d.pop("aggregatedPricing", UNSET)

        bill_to = d.pop("billTo", UNSET)

        pricing_table = d.pop("pricingTable", UNSET)

        net_suite_default_item_code = d.pop("netSuiteDefaultItemCode", UNSET)

        net_suite_default_description = d.pop("netSuiteDefaultDescription", UNSET)

        tenant_billing_settings = cls(
            discount=discount,
            monthly_minimum=monthly_minimum,
            aggregated_pricing=aggregated_pricing,
            bill_to=bill_to,
            pricing_table=pricing_table,
            net_suite_default_item_code=net_suite_default_item_code,
            net_suite_default_description=net_suite_default_description,
        )

        return tenant_billing_settings

