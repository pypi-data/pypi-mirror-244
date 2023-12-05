import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_status import BackgroundTaskStatus
from ..models.external_data_provider import ExternalDataProvider
from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.pay_run_payment import PayRunPayment
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayrunPaymentsReport")

@attr.s(auto_attribs=True)
class PayrunPaymentsReport:
    """After finalising a PayRun, employees need to actually be paid.
This model is returned by the Reports API and is used to provide details of a payment that needs to be made.

    Attributes:
        payments (Union[Unset, None, List[PayRunPayment]]):
        status (Union[Unset, BackgroundTaskStatus]):
        status_message (Union[Unset, None, str]): [readonly] A message to elaborate on the Status
        link (Union[Unset, None, str]): [readonly]  If available, a link to the payments in an ExternalDataProvider
        connected_external_data_provider (Union[Unset, ExternalDataProvider]):
        employer (Union[Unset, Item]):
        pay_period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]):
        period (Union[Unset, int]):
        period_to (Union[Unset, int]):
        start_period_name (Union[Unset, None, str]):
        end_period_name (Union[Unset, None, str]):
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
        is_draft (Union[Unset, bool]):
    """

    payments: Union[Unset, None, List[PayRunPayment]] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    link: Union[Unset, None, str] = UNSET
    connected_external_data_provider: Union[Unset, ExternalDataProvider] = UNSET
    employer: Union[Unset, Item] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET
    period_to: Union[Unset, int] = UNSET
    start_period_name: Union[Unset, None, str] = UNSET
    end_period_name: Union[Unset, None, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    is_draft: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        payments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.payments, Unset):
            if self.payments is None:
                payments = None
            else:
                payments = []
                for payments_item_data in self.payments:
                    payments_item = payments_item_data.to_dict()

                    payments.append(payments_item)




        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message
        link = self.link
        connected_external_data_provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.connected_external_data_provider, Unset):
            connected_external_data_provider = self.connected_external_data_provider.to_dict()

        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period
        period_to = self.period_to
        start_period_name = self.start_period_name
        end_period_name = self.end_period_name
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if payments is not UNSET:
            field_dict["payments"] = payments
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if link is not UNSET:
            field_dict["link"] = link
        if connected_external_data_provider is not UNSET:
            field_dict["connectedExternalDataProvider"] = connected_external_data_provider
        if employer is not UNSET:
            field_dict["employer"] = employer
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period
        if period_to is not UNSET:
            field_dict["periodTo"] = period_to
        if start_period_name is not UNSET:
            field_dict["startPeriodName"] = start_period_name
        if end_period_name is not UNSET:
            field_dict["endPeriodName"] = end_period_name
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if is_draft is not UNSET:
            field_dict["isDraft"] = is_draft

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payments = []
        _payments = d.pop("payments", UNSET)
        for payments_item_data in (_payments or []):
            payments_item = PayRunPayment.from_dict(payments_item_data)



            payments.append(payments_item)


        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)




        status_message = d.pop("statusMessage", UNSET)

        link = d.pop("link", UNSET)

        _connected_external_data_provider = d.pop("connectedExternalDataProvider", UNSET)
        connected_external_data_provider: Union[Unset, ExternalDataProvider]
        if isinstance(_connected_external_data_provider,  Unset):
            connected_external_data_provider = UNSET
        else:
            connected_external_data_provider = ExternalDataProvider.from_dict(_connected_external_data_provider)




        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, Item]
        if isinstance(_employer,  Unset):
            employer = UNSET
        else:
            employer = Item.from_dict(_employer)




        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period,  Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)




        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

        period_to = d.pop("periodTo", UNSET)

        start_period_name = d.pop("startPeriodName", UNSET)

        end_period_name = d.pop("endPeriodName", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date,  Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()




        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.date]
        if isinstance(_end_date,  Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()




        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report,  Unset):
            report = UNSET
        else:
            report = Report(_report)




        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)




        is_draft = d.pop("isDraft", UNSET)

        payrun_payments_report = cls(
            payments=payments,
            status=status,
            status_message=status_message,
            link=link,
            connected_external_data_provider=connected_external_data_provider,
            employer=employer,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
            period_to=period_to,
            start_period_name=start_period_name,
            end_period_name=end_period_name,
            start_date=start_date,
            end_date=end_date,
            report=report,
            tax_year=tax_year,
            is_draft=is_draft,
        )

        return payrun_payments_report

