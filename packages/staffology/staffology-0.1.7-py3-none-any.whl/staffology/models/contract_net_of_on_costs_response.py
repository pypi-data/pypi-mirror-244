from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.contract_net_of_on_costs_simulation_response import ContractNetOfOnCostsSimulationResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractNetOfOnCostsResponse")

@attr.s(auto_attribs=True)
class ContractNetOfOnCostsResponse:
    """
    Attributes:
        salary (Union[Unset, float]):
        holiday_pay (Union[Unset, float]):
        employers_pension_contribution (Union[Unset, float]):
        employees_pension_contribution (Union[Unset, float]):
        employers_ni (Union[Unset, float]):
        apprenticeship_levy (Union[Unset, float]):
        gross_daily_rate (Union[Unset, float]):
        total_fees (Union[Unset, float]):
        number_of_days (Union[Unset, float]):
        simulation (Union[Unset, ContractNetOfOnCostsSimulationResponse]):
        hol_inclusive_simulation (Union[Unset, ContractNetOfOnCostsSimulationResponse]):
    """

    salary: Union[Unset, float] = UNSET
    holiday_pay: Union[Unset, float] = UNSET
    employers_pension_contribution: Union[Unset, float] = UNSET
    employees_pension_contribution: Union[Unset, float] = UNSET
    employers_ni: Union[Unset, float] = UNSET
    apprenticeship_levy: Union[Unset, float] = UNSET
    gross_daily_rate: Union[Unset, float] = UNSET
    total_fees: Union[Unset, float] = UNSET
    number_of_days: Union[Unset, float] = UNSET
    simulation: Union[Unset, ContractNetOfOnCostsSimulationResponse] = UNSET
    hol_inclusive_simulation: Union[Unset, ContractNetOfOnCostsSimulationResponse] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        salary = self.salary
        holiday_pay = self.holiday_pay
        employers_pension_contribution = self.employers_pension_contribution
        employees_pension_contribution = self.employees_pension_contribution
        employers_ni = self.employers_ni
        apprenticeship_levy = self.apprenticeship_levy
        gross_daily_rate = self.gross_daily_rate
        total_fees = self.total_fees
        number_of_days = self.number_of_days
        simulation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.simulation, Unset):
            simulation = self.simulation.to_dict()

        hol_inclusive_simulation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hol_inclusive_simulation, Unset):
            hol_inclusive_simulation = self.hol_inclusive_simulation.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if salary is not UNSET:
            field_dict["salary"] = salary
        if holiday_pay is not UNSET:
            field_dict["holidayPay"] = holiday_pay
        if employers_pension_contribution is not UNSET:
            field_dict["employersPensionContribution"] = employers_pension_contribution
        if employees_pension_contribution is not UNSET:
            field_dict["employeesPensionContribution"] = employees_pension_contribution
        if employers_ni is not UNSET:
            field_dict["employersNi"] = employers_ni
        if apprenticeship_levy is not UNSET:
            field_dict["apprenticeshipLevy"] = apprenticeship_levy
        if gross_daily_rate is not UNSET:
            field_dict["grossDailyRate"] = gross_daily_rate
        if total_fees is not UNSET:
            field_dict["totalFees"] = total_fees
        if number_of_days is not UNSET:
            field_dict["numberOfDays"] = number_of_days
        if simulation is not UNSET:
            field_dict["simulation"] = simulation
        if hol_inclusive_simulation is not UNSET:
            field_dict["holInclusiveSimulation"] = hol_inclusive_simulation

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        salary = d.pop("salary", UNSET)

        holiday_pay = d.pop("holidayPay", UNSET)

        employers_pension_contribution = d.pop("employersPensionContribution", UNSET)

        employees_pension_contribution = d.pop("employeesPensionContribution", UNSET)

        employers_ni = d.pop("employersNi", UNSET)

        apprenticeship_levy = d.pop("apprenticeshipLevy", UNSET)

        gross_daily_rate = d.pop("grossDailyRate", UNSET)

        total_fees = d.pop("totalFees", UNSET)

        number_of_days = d.pop("numberOfDays", UNSET)

        _simulation = d.pop("simulation", UNSET)
        simulation: Union[Unset, ContractNetOfOnCostsSimulationResponse]
        if isinstance(_simulation,  Unset):
            simulation = UNSET
        else:
            simulation = ContractNetOfOnCostsSimulationResponse.from_dict(_simulation)




        _hol_inclusive_simulation = d.pop("holInclusiveSimulation", UNSET)
        hol_inclusive_simulation: Union[Unset, ContractNetOfOnCostsSimulationResponse]
        if isinstance(_hol_inclusive_simulation,  Unset):
            hol_inclusive_simulation = UNSET
        else:
            hol_inclusive_simulation = ContractNetOfOnCostsSimulationResponse.from_dict(_hol_inclusive_simulation)




        contract_net_of_on_costs_response = cls(
            salary=salary,
            holiday_pay=holiday_pay,
            employers_pension_contribution=employers_pension_contribution,
            employees_pension_contribution=employees_pension_contribution,
            employers_ni=employers_ni,
            apprenticeship_levy=apprenticeship_levy,
            gross_daily_rate=gross_daily_rate,
            total_fees=total_fees,
            number_of_days=number_of_days,
            simulation=simulation,
            hol_inclusive_simulation=hol_inclusive_simulation,
        )

        return contract_net_of_on_costs_response

