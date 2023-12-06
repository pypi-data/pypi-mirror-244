import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_net_of_on_costs_response import ContractNetOfOnCostsResponse
from ...models.pay_periods import PayPeriods
from ...models.pension_rule import PensionRule
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    notional_day_rate: float,
    calculation_date: Union[Unset, None, datetime.datetime] = UNSET,
    fee: float,
    fee_is_percentage: bool,
    apprenticeship_levy_rate_override: Union[Unset, None, float] = UNSET,
    employers_pension_contribution: float,
    employers_pension_contribution_is_percentage: bool,
    employees_pension_contribution: float,
    employees_pension_contribution_is_percentage: bool,
    use_ae_bandings: bool,
    holiday_weeks: float,
    days_worked_per_week: int,
    pay_period: PayPeriods,
    pension_rule: Union[Unset, None, PensionRule] = UNSET,

) -> Dict[str, Any]:
    url = "{}/tools/calculate-net-of-on-costs".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["NotionalDayRate"] = notional_day_rate


    json_calculation_date: Union[Unset, None, str] = UNSET
    if not isinstance(calculation_date, Unset):
        json_calculation_date = calculation_date.isoformat() if calculation_date else None

    params["CalculationDate"] = json_calculation_date


    params["Fee"] = fee


    params["FeeIsPercentage"] = fee_is_percentage


    params["ApprenticeshipLevyRateOverride"] = apprenticeship_levy_rate_override


    params["EmployersPensionContribution"] = employers_pension_contribution


    params["EmployersPensionContributionIsPercentage"] = employers_pension_contribution_is_percentage


    params["EmployeesPensionContribution"] = employees_pension_contribution


    params["EmployeesPensionContributionIsPercentage"] = employees_pension_contribution_is_percentage


    params["UseAeBandings"] = use_ae_bandings


    params["HolidayWeeks"] = holiday_weeks


    params["DaysWorkedPerWeek"] = days_worked_per_week


    json_pay_period = pay_period.value

    params["PayPeriod"] = json_pay_period


    json_pension_rule: Union[Unset, None, str] = UNSET
    if not isinstance(pension_rule, Unset):
        json_pension_rule = pension_rule.value if pension_rule else None

    params["PensionRule"] = json_pension_rule



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractNetOfOnCostsResponse]]:
    if response.status_code == 200:
        response_200 = ContractNetOfOnCostsResponse.from_dict(response.json())



        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractNetOfOnCostsResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    notional_day_rate: float,
    calculation_date: Union[Unset, None, datetime.datetime] = UNSET,
    fee: float,
    fee_is_percentage: bool,
    apprenticeship_levy_rate_override: Union[Unset, None, float] = UNSET,
    employers_pension_contribution: float,
    employers_pension_contribution_is_percentage: bool,
    employees_pension_contribution: float,
    employees_pension_contribution_is_percentage: bool,
    use_ae_bandings: bool,
    holiday_weeks: float,
    days_worked_per_week: int,
    pay_period: PayPeriods,
    pension_rule: Union[Unset, None, PensionRule] = UNSET,

) -> Response[Union[Any, ContractNetOfOnCostsResponse]]:
    """Calculate Net of On Costs

     Calculate the Gross Daily Pay and typical Net Costs for an employee.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        notional_day_rate (float):
        calculation_date (Union[Unset, None, datetime.datetime]):
        fee (float):
        fee_is_percentage (bool):
        apprenticeship_levy_rate_override (Union[Unset, None, float]):
        employers_pension_contribution (float):
        employers_pension_contribution_is_percentage (bool):
        employees_pension_contribution (float):
        employees_pension_contribution_is_percentage (bool):
        use_ae_bandings (bool):
        holiday_weeks (float):
        days_worked_per_week (int):
        pay_period (PayPeriods):
        pension_rule (Union[Unset, None, PensionRule]):

    Returns:
        Response[Union[Any, ContractNetOfOnCostsResponse]]
    """


    kwargs = _get_kwargs(
        client=client,
notional_day_rate=notional_day_rate,
calculation_date=calculation_date,
fee=fee,
fee_is_percentage=fee_is_percentage,
apprenticeship_levy_rate_override=apprenticeship_levy_rate_override,
employers_pension_contribution=employers_pension_contribution,
employers_pension_contribution_is_percentage=employers_pension_contribution_is_percentage,
employees_pension_contribution=employees_pension_contribution,
employees_pension_contribution_is_percentage=employees_pension_contribution_is_percentage,
use_ae_bandings=use_ae_bandings,
holiday_weeks=holiday_weeks,
days_worked_per_week=days_worked_per_week,
pay_period=pay_period,
pension_rule=pension_rule,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    notional_day_rate: float,
    calculation_date: Union[Unset, None, datetime.datetime] = UNSET,
    fee: float,
    fee_is_percentage: bool,
    apprenticeship_levy_rate_override: Union[Unset, None, float] = UNSET,
    employers_pension_contribution: float,
    employers_pension_contribution_is_percentage: bool,
    employees_pension_contribution: float,
    employees_pension_contribution_is_percentage: bool,
    use_ae_bandings: bool,
    holiday_weeks: float,
    days_worked_per_week: int,
    pay_period: PayPeriods,
    pension_rule: Union[Unset, None, PensionRule] = UNSET,

) -> Optional[Union[Any, ContractNetOfOnCostsResponse]]:
    """Calculate Net of On Costs

     Calculate the Gross Daily Pay and typical Net Costs for an employee.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        notional_day_rate (float):
        calculation_date (Union[Unset, None, datetime.datetime]):
        fee (float):
        fee_is_percentage (bool):
        apprenticeship_levy_rate_override (Union[Unset, None, float]):
        employers_pension_contribution (float):
        employers_pension_contribution_is_percentage (bool):
        employees_pension_contribution (float):
        employees_pension_contribution_is_percentage (bool):
        use_ae_bandings (bool):
        holiday_weeks (float):
        days_worked_per_week (int):
        pay_period (PayPeriods):
        pension_rule (Union[Unset, None, PensionRule]):

    Returns:
        Response[Union[Any, ContractNetOfOnCostsResponse]]
    """


    return sync_detailed(
        client=client,
notional_day_rate=notional_day_rate,
calculation_date=calculation_date,
fee=fee,
fee_is_percentage=fee_is_percentage,
apprenticeship_levy_rate_override=apprenticeship_levy_rate_override,
employers_pension_contribution=employers_pension_contribution,
employers_pension_contribution_is_percentage=employers_pension_contribution_is_percentage,
employees_pension_contribution=employees_pension_contribution,
employees_pension_contribution_is_percentage=employees_pension_contribution_is_percentage,
use_ae_bandings=use_ae_bandings,
holiday_weeks=holiday_weeks,
days_worked_per_week=days_worked_per_week,
pay_period=pay_period,
pension_rule=pension_rule,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    notional_day_rate: float,
    calculation_date: Union[Unset, None, datetime.datetime] = UNSET,
    fee: float,
    fee_is_percentage: bool,
    apprenticeship_levy_rate_override: Union[Unset, None, float] = UNSET,
    employers_pension_contribution: float,
    employers_pension_contribution_is_percentage: bool,
    employees_pension_contribution: float,
    employees_pension_contribution_is_percentage: bool,
    use_ae_bandings: bool,
    holiday_weeks: float,
    days_worked_per_week: int,
    pay_period: PayPeriods,
    pension_rule: Union[Unset, None, PensionRule] = UNSET,

) -> Response[Union[Any, ContractNetOfOnCostsResponse]]:
    """Calculate Net of On Costs

     Calculate the Gross Daily Pay and typical Net Costs for an employee.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        notional_day_rate (float):
        calculation_date (Union[Unset, None, datetime.datetime]):
        fee (float):
        fee_is_percentage (bool):
        apprenticeship_levy_rate_override (Union[Unset, None, float]):
        employers_pension_contribution (float):
        employers_pension_contribution_is_percentage (bool):
        employees_pension_contribution (float):
        employees_pension_contribution_is_percentage (bool):
        use_ae_bandings (bool):
        holiday_weeks (float):
        days_worked_per_week (int):
        pay_period (PayPeriods):
        pension_rule (Union[Unset, None, PensionRule]):

    Returns:
        Response[Union[Any, ContractNetOfOnCostsResponse]]
    """


    kwargs = _get_kwargs(
        client=client,
notional_day_rate=notional_day_rate,
calculation_date=calculation_date,
fee=fee,
fee_is_percentage=fee_is_percentage,
apprenticeship_levy_rate_override=apprenticeship_levy_rate_override,
employers_pension_contribution=employers_pension_contribution,
employers_pension_contribution_is_percentage=employers_pension_contribution_is_percentage,
employees_pension_contribution=employees_pension_contribution,
employees_pension_contribution_is_percentage=employees_pension_contribution_is_percentage,
use_ae_bandings=use_ae_bandings,
holiday_weeks=holiday_weeks,
days_worked_per_week=days_worked_per_week,
pay_period=pay_period,
pension_rule=pension_rule,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    notional_day_rate: float,
    calculation_date: Union[Unset, None, datetime.datetime] = UNSET,
    fee: float,
    fee_is_percentage: bool,
    apprenticeship_levy_rate_override: Union[Unset, None, float] = UNSET,
    employers_pension_contribution: float,
    employers_pension_contribution_is_percentage: bool,
    employees_pension_contribution: float,
    employees_pension_contribution_is_percentage: bool,
    use_ae_bandings: bool,
    holiday_weeks: float,
    days_worked_per_week: int,
    pay_period: PayPeriods,
    pension_rule: Union[Unset, None, PensionRule] = UNSET,

) -> Optional[Union[Any, ContractNetOfOnCostsResponse]]:
    """Calculate Net of On Costs

     Calculate the Gross Daily Pay and typical Net Costs for an employee.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        notional_day_rate (float):
        calculation_date (Union[Unset, None, datetime.datetime]):
        fee (float):
        fee_is_percentage (bool):
        apprenticeship_levy_rate_override (Union[Unset, None, float]):
        employers_pension_contribution (float):
        employers_pension_contribution_is_percentage (bool):
        employees_pension_contribution (float):
        employees_pension_contribution_is_percentage (bool):
        use_ae_bandings (bool):
        holiday_weeks (float):
        days_worked_per_week (int):
        pay_period (PayPeriods):
        pension_rule (Union[Unset, None, PensionRule]):

    Returns:
        Response[Union[Any, ContractNetOfOnCostsResponse]]
    """


    return (await asyncio_detailed(
        client=client,
notional_day_rate=notional_day_rate,
calculation_date=calculation_date,
fee=fee,
fee_is_percentage=fee_is_percentage,
apprenticeship_levy_rate_override=apprenticeship_levy_rate_override,
employers_pension_contribution=employers_pension_contribution,
employers_pension_contribution_is_percentage=employers_pension_contribution_is_percentage,
employees_pension_contribution=employees_pension_contribution,
employees_pension_contribution_is_percentage=employees_pension_contribution_is_percentage,
use_ae_bandings=use_ae_bandings,
holiday_weeks=holiday_weeks,
days_worked_per_week=days_worked_per_week,
pay_period=pay_period,
pension_rule=pension_rule,

    )).parsed

