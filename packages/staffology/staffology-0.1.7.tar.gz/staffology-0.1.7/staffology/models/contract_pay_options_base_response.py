from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.contract_pay_line_response import ContractPayLineResponse
from ..models.mileage_vehicle_type import MileageVehicleType
from ..models.pay_basis import PayBasis
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPayOptionsBaseResponse")

@attr.s(auto_attribs=True)
class ContractPayOptionsBaseResponse:
    """
    Attributes:
        regular_pay_lines (Union[Unset, None, List[ContractPayLineResponse]]): These are used to make
            additions/deductions to the pay for this Employee.
            You do not need to include Pension, Tax, NI,  Loan Repayments, etc as these will all be automatically created.
        basis (Union[Unset, PayBasis]):
        national_minimum_wage (Union[Unset, bool]):
        pay_code (Union[Unset, None, str]): If you want the Employees pay to be allocated to a code other than BASIC,
            specify it here
        mileage_vehicle_type (Union[Unset, MileageVehicleType]):
        maps_miles (Union[Unset, None, int]): The number of miles to pay for as Mileage Allowance Payments
        pay_amount (Union[Unset, float]): The amount the Employee is regularly paid each period
        pay_amount_multiplier (Union[Unset, float]): This property is irrelevant if the basis is Monthly.
            But if the basis is Daily or Hourly then this property sets how many days/hours the employee should be paid for
            in the period.
        base_hourly_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base hourly rate. Eg Overtime.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        base_daily_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base daily rate. Eg sick.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        auto_adjust_for_leave (Union[Unset, bool]): Automatically reduce the PayAmount when the Employee has Leave that
            is either Not Paid or has Statutory Pay.
            Can only be set to True if the Basis is Monthly (ie, employee is not paid an hourly or daily rate).
            If set to false then you must manually reduce their payment to reflect any Leave
        ni_table (Union[Unset, str]):
    """

    regular_pay_lines: Union[Unset, None, List[ContractPayLineResponse]] = UNSET
    basis: Union[Unset, PayBasis] = UNSET
    national_minimum_wage: Union[Unset, bool] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    mileage_vehicle_type: Union[Unset, MileageVehicleType] = UNSET
    maps_miles: Union[Unset, None, int] = UNSET
    pay_amount: Union[Unset, float] = UNSET
    pay_amount_multiplier: Union[Unset, float] = UNSET
    base_hourly_rate: Union[Unset, float] = UNSET
    base_daily_rate: Union[Unset, float] = UNSET
    auto_adjust_for_leave: Union[Unset, bool] = UNSET
    ni_table: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        regular_pay_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.regular_pay_lines, Unset):
            if self.regular_pay_lines is None:
                regular_pay_lines = None
            else:
                regular_pay_lines = []
                for regular_pay_lines_item_data in self.regular_pay_lines:
                    regular_pay_lines_item = regular_pay_lines_item_data.to_dict()

                    regular_pay_lines.append(regular_pay_lines_item)




        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        national_minimum_wage = self.national_minimum_wage
        pay_code = self.pay_code
        mileage_vehicle_type: Union[Unset, str] = UNSET
        if not isinstance(self.mileage_vehicle_type, Unset):
            mileage_vehicle_type = self.mileage_vehicle_type.value

        maps_miles = self.maps_miles
        pay_amount = self.pay_amount
        pay_amount_multiplier = self.pay_amount_multiplier
        base_hourly_rate = self.base_hourly_rate
        base_daily_rate = self.base_daily_rate
        auto_adjust_for_leave = self.auto_adjust_for_leave
        ni_table = self.ni_table

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if regular_pay_lines is not UNSET:
            field_dict["regularPayLines"] = regular_pay_lines
        if basis is not UNSET:
            field_dict["basis"] = basis
        if national_minimum_wage is not UNSET:
            field_dict["nationalMinimumWage"] = national_minimum_wage
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if mileage_vehicle_type is not UNSET:
            field_dict["mileageVehicleType"] = mileage_vehicle_type
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if pay_amount is not UNSET:
            field_dict["payAmount"] = pay_amount
        if pay_amount_multiplier is not UNSET:
            field_dict["payAmountMultiplier"] = pay_amount_multiplier
        if base_hourly_rate is not UNSET:
            field_dict["baseHourlyRate"] = base_hourly_rate
        if base_daily_rate is not UNSET:
            field_dict["baseDailyRate"] = base_daily_rate
        if auto_adjust_for_leave is not UNSET:
            field_dict["autoAdjustForLeave"] = auto_adjust_for_leave
        if ni_table is not UNSET:
            field_dict["niTable"] = ni_table

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        regular_pay_lines = []
        _regular_pay_lines = d.pop("regularPayLines", UNSET)
        for regular_pay_lines_item_data in (_regular_pay_lines or []):
            regular_pay_lines_item = ContractPayLineResponse.from_dict(regular_pay_lines_item_data)



            regular_pay_lines.append(regular_pay_lines_item)


        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, PayBasis]
        if isinstance(_basis,  Unset):
            basis = UNSET
        else:
            basis = PayBasis(_basis)




        national_minimum_wage = d.pop("nationalMinimumWage", UNSET)

        pay_code = d.pop("payCode", UNSET)

        _mileage_vehicle_type = d.pop("mileageVehicleType", UNSET)
        mileage_vehicle_type: Union[Unset, MileageVehicleType]
        if isinstance(_mileage_vehicle_type,  Unset):
            mileage_vehicle_type = UNSET
        else:
            mileage_vehicle_type = MileageVehicleType(_mileage_vehicle_type)




        maps_miles = d.pop("mapsMiles", UNSET)

        pay_amount = d.pop("payAmount", UNSET)

        pay_amount_multiplier = d.pop("payAmountMultiplier", UNSET)

        base_hourly_rate = d.pop("baseHourlyRate", UNSET)

        base_daily_rate = d.pop("baseDailyRate", UNSET)

        auto_adjust_for_leave = d.pop("autoAdjustForLeave", UNSET)

        ni_table = d.pop("niTable", UNSET)

        contract_pay_options_base_response = cls(
            regular_pay_lines=regular_pay_lines,
            basis=basis,
            national_minimum_wage=national_minimum_wage,
            pay_code=pay_code,
            mileage_vehicle_type=mileage_vehicle_type,
            maps_miles=maps_miles,
            pay_amount=pay_amount,
            pay_amount_multiplier=pay_amount_multiplier,
            base_hourly_rate=base_hourly_rate,
            base_daily_rate=base_daily_rate,
            auto_adjust_for_leave=auto_adjust_for_leave,
            ni_table=ni_table,
        )

        return contract_pay_options_base_response

