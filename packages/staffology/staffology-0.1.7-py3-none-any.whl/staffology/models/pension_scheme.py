from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.bank_details import BankDetails
from ..models.day_of_week import DayOfWeek
from ..models.external_data_company import ExternalDataCompany
from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.pay_method import PayMethod
from ..models.payment_date_rule import PaymentDateRule
from ..models.pension_administrator import PensionAdministrator
from ..models.pension_pay_code import PensionPayCode
from ..models.pension_provider import PensionProvider
from ..models.pension_rule import PensionRule
from ..models.pension_scheme_report_options_lgps_civica_upm import PensionSchemeReportOptionsLgpsCivicaUpm
from ..models.pension_scheme_report_options_lgps_i_connect import PensionSchemeReportOptionsLgpsIConnect
from ..models.worker_group import WorkerGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionScheme")

@attr.s(auto_attribs=True)
class PensionScheme:
    """
    Attributes:
        name (str):
        provider (Union[Unset, PensionProvider]):
        administrator (Union[Unset, PensionAdministrator]):
        pension_rule (Union[Unset, PensionRule]):
        qualifying_scheme (Union[Unset, bool]): Set to true if this is a Qualifying Scheme for Auto Enrolment
        disable_ae_letters (Union[Unset, bool]): Set to true if the provider deals with AutoEnrolment Letters and
            therefore the system should not generate them
        subtract_basic_rate_tax (Union[Unset, bool]):
        pay_method (Union[Unset, PayMethod]):
        bank_details (Union[Unset, BankDetails]):
        use_custom_pay_codes (Union[Unset, bool]): If set to true then rather than using the setting on the PayCode to
            determine if the pay is pensionable
            we'll instead treat it as pensionable if the Code is included in CustomPayCodes
        custom_pay_codes (Union[Unset, None, List[str]]): If UseCustomPayCodes is set to true then this contains a list
            of PayCodes.Code
            that we'll treat as being pensionable.
        worker_groups (Union[Unset, None, List[WorkerGroup]]): A list of WorkerGroups for this Pension. There must
            always be at least one WorkerGroup
        external_data_provider_id (Union[Unset, ExternalDataProviderId]):
        external_data_company (Union[Unset, ExternalDataCompany]): When we retrieve data from an ExternalDataProvider we
            normalise it so that regardless of the provider the models are the same.
            This model is used to represent a Company in an ExternalDataProvider
        pay_code_type (Union[Unset, PensionPayCode]):
        pay_code_set_unique_id (Union[Unset, None, str]):
        payment_date_rule (Union[Unset, PaymentDateRule]):
        payment_date_day_of_week (Union[Unset, DayOfWeek]):
        payment_date_day_of_month (Union[Unset, None, int]):
        report_options_lgps_i_connect (Union[Unset, PensionSchemeReportOptionsLgpsIConnect]):
        report_options_lgps_civica_upm (Union[Unset, PensionSchemeReportOptionsLgpsCivicaUpm]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    provider: Union[Unset, PensionProvider] = UNSET
    administrator: Union[Unset, PensionAdministrator] = UNSET
    pension_rule: Union[Unset, PensionRule] = UNSET
    qualifying_scheme: Union[Unset, bool] = UNSET
    disable_ae_letters: Union[Unset, bool] = UNSET
    subtract_basic_rate_tax: Union[Unset, bool] = UNSET
    pay_method: Union[Unset, PayMethod] = UNSET
    bank_details: Union[Unset, BankDetails] = UNSET
    use_custom_pay_codes: Union[Unset, bool] = UNSET
    custom_pay_codes: Union[Unset, None, List[str]] = UNSET
    worker_groups: Union[Unset, None, List[WorkerGroup]] = UNSET
    external_data_provider_id: Union[Unset, ExternalDataProviderId] = UNSET
    external_data_company: Union[Unset, ExternalDataCompany] = UNSET
    pay_code_type: Union[Unset, PensionPayCode] = UNSET
    pay_code_set_unique_id: Union[Unset, None, str] = UNSET
    payment_date_rule: Union[Unset, PaymentDateRule] = UNSET
    payment_date_day_of_week: Union[Unset, DayOfWeek] = UNSET
    payment_date_day_of_month: Union[Unset, None, int] = UNSET
    report_options_lgps_i_connect: Union[Unset, PensionSchemeReportOptionsLgpsIConnect] = UNSET
    report_options_lgps_civica_upm: Union[Unset, PensionSchemeReportOptionsLgpsCivicaUpm] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        administrator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.administrator, Unset):
            administrator = self.administrator.to_dict()

        pension_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pension_rule, Unset):
            pension_rule = self.pension_rule.value

        qualifying_scheme = self.qualifying_scheme
        disable_ae_letters = self.disable_ae_letters
        subtract_basic_rate_tax = self.subtract_basic_rate_tax
        pay_method: Union[Unset, str] = UNSET
        if not isinstance(self.pay_method, Unset):
            pay_method = self.pay_method.value

        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        use_custom_pay_codes = self.use_custom_pay_codes
        custom_pay_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.custom_pay_codes, Unset):
            if self.custom_pay_codes is None:
                custom_pay_codes = None
            else:
                custom_pay_codes = self.custom_pay_codes




        worker_groups: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.worker_groups, Unset):
            if self.worker_groups is None:
                worker_groups = None
            else:
                worker_groups = []
                for worker_groups_item_data in self.worker_groups:
                    worker_groups_item = worker_groups_item_data.to_dict()

                    worker_groups.append(worker_groups_item)




        external_data_provider_id: Union[Unset, str] = UNSET
        if not isinstance(self.external_data_provider_id, Unset):
            external_data_provider_id = self.external_data_provider_id.value

        external_data_company: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.external_data_company, Unset):
            external_data_company = self.external_data_company.to_dict()

        pay_code_type: Union[Unset, str] = UNSET
        if not isinstance(self.pay_code_type, Unset):
            pay_code_type = self.pay_code_type.value

        pay_code_set_unique_id = self.pay_code_set_unique_id
        payment_date_rule: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date_rule, Unset):
            payment_date_rule = self.payment_date_rule.value

        payment_date_day_of_week: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date_day_of_week, Unset):
            payment_date_day_of_week = self.payment_date_day_of_week.value

        payment_date_day_of_month = self.payment_date_day_of_month
        report_options_lgps_i_connect: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report_options_lgps_i_connect, Unset):
            report_options_lgps_i_connect = self.report_options_lgps_i_connect.to_dict()

        report_options_lgps_civica_upm: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.report_options_lgps_civica_upm, Unset):
            report_options_lgps_civica_upm = self.report_options_lgps_civica_upm.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if provider is not UNSET:
            field_dict["provider"] = provider
        if administrator is not UNSET:
            field_dict["administrator"] = administrator
        if pension_rule is not UNSET:
            field_dict["pensionRule"] = pension_rule
        if qualifying_scheme is not UNSET:
            field_dict["qualifyingScheme"] = qualifying_scheme
        if disable_ae_letters is not UNSET:
            field_dict["disableAeLetters"] = disable_ae_letters
        if subtract_basic_rate_tax is not UNSET:
            field_dict["subtractBasicRateTax"] = subtract_basic_rate_tax
        if pay_method is not UNSET:
            field_dict["payMethod"] = pay_method
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if use_custom_pay_codes is not UNSET:
            field_dict["useCustomPayCodes"] = use_custom_pay_codes
        if custom_pay_codes is not UNSET:
            field_dict["customPayCodes"] = custom_pay_codes
        if worker_groups is not UNSET:
            field_dict["workerGroups"] = worker_groups
        if external_data_provider_id is not UNSET:
            field_dict["externalDataProviderId"] = external_data_provider_id
        if external_data_company is not UNSET:
            field_dict["externalDataCompany"] = external_data_company
        if pay_code_type is not UNSET:
            field_dict["payCodeType"] = pay_code_type
        if pay_code_set_unique_id is not UNSET:
            field_dict["payCodeSetUniqueId"] = pay_code_set_unique_id
        if payment_date_rule is not UNSET:
            field_dict["paymentDateRule"] = payment_date_rule
        if payment_date_day_of_week is not UNSET:
            field_dict["paymentDateDayOfWeek"] = payment_date_day_of_week
        if payment_date_day_of_month is not UNSET:
            field_dict["paymentDateDayOfMonth"] = payment_date_day_of_month
        if report_options_lgps_i_connect is not UNSET:
            field_dict["reportOptionsLgpsIConnect"] = report_options_lgps_i_connect
        if report_options_lgps_civica_upm is not UNSET:
            field_dict["reportOptionsLgpsCivicaUpm"] = report_options_lgps_civica_upm
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, PensionProvider]
        if isinstance(_provider,  Unset):
            provider = UNSET
        else:
            provider = PensionProvider.from_dict(_provider)




        _administrator = d.pop("administrator", UNSET)
        administrator: Union[Unset, PensionAdministrator]
        if isinstance(_administrator,  Unset):
            administrator = UNSET
        else:
            administrator = PensionAdministrator.from_dict(_administrator)




        _pension_rule = d.pop("pensionRule", UNSET)
        pension_rule: Union[Unset, PensionRule]
        if isinstance(_pension_rule,  Unset):
            pension_rule = UNSET
        else:
            pension_rule = PensionRule(_pension_rule)




        qualifying_scheme = d.pop("qualifyingScheme", UNSET)

        disable_ae_letters = d.pop("disableAeLetters", UNSET)

        subtract_basic_rate_tax = d.pop("subtractBasicRateTax", UNSET)

        _pay_method = d.pop("payMethod", UNSET)
        pay_method: Union[Unset, PayMethod]
        if isinstance(_pay_method,  Unset):
            pay_method = UNSET
        else:
            pay_method = PayMethod(_pay_method)




        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details,  Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)




        use_custom_pay_codes = d.pop("useCustomPayCodes", UNSET)

        custom_pay_codes = cast(List[str], d.pop("customPayCodes", UNSET))


        worker_groups = []
        _worker_groups = d.pop("workerGroups", UNSET)
        for worker_groups_item_data in (_worker_groups or []):
            worker_groups_item = WorkerGroup.from_dict(worker_groups_item_data)



            worker_groups.append(worker_groups_item)


        _external_data_provider_id = d.pop("externalDataProviderId", UNSET)
        external_data_provider_id: Union[Unset, ExternalDataProviderId]
        if isinstance(_external_data_provider_id,  Unset):
            external_data_provider_id = UNSET
        else:
            external_data_provider_id = ExternalDataProviderId(_external_data_provider_id)




        _external_data_company = d.pop("externalDataCompany", UNSET)
        external_data_company: Union[Unset, ExternalDataCompany]
        if isinstance(_external_data_company,  Unset):
            external_data_company = UNSET
        else:
            external_data_company = ExternalDataCompany.from_dict(_external_data_company)




        _pay_code_type = d.pop("payCodeType", UNSET)
        pay_code_type: Union[Unset, PensionPayCode]
        if isinstance(_pay_code_type,  Unset):
            pay_code_type = UNSET
        else:
            pay_code_type = PensionPayCode(_pay_code_type)




        pay_code_set_unique_id = d.pop("payCodeSetUniqueId", UNSET)

        _payment_date_rule = d.pop("paymentDateRule", UNSET)
        payment_date_rule: Union[Unset, PaymentDateRule]
        if isinstance(_payment_date_rule,  Unset):
            payment_date_rule = UNSET
        else:
            payment_date_rule = PaymentDateRule(_payment_date_rule)




        _payment_date_day_of_week = d.pop("paymentDateDayOfWeek", UNSET)
        payment_date_day_of_week: Union[Unset, DayOfWeek]
        if isinstance(_payment_date_day_of_week,  Unset):
            payment_date_day_of_week = UNSET
        else:
            payment_date_day_of_week = DayOfWeek(_payment_date_day_of_week)




        payment_date_day_of_month = d.pop("paymentDateDayOfMonth", UNSET)

        _report_options_lgps_i_connect = d.pop("reportOptionsLgpsIConnect", UNSET)
        report_options_lgps_i_connect: Union[Unset, PensionSchemeReportOptionsLgpsIConnect]
        if isinstance(_report_options_lgps_i_connect,  Unset):
            report_options_lgps_i_connect = UNSET
        else:
            report_options_lgps_i_connect = PensionSchemeReportOptionsLgpsIConnect.from_dict(_report_options_lgps_i_connect)




        _report_options_lgps_civica_upm = d.pop("reportOptionsLgpsCivicaUpm", UNSET)
        report_options_lgps_civica_upm: Union[Unset, PensionSchemeReportOptionsLgpsCivicaUpm]
        if isinstance(_report_options_lgps_civica_upm,  Unset):
            report_options_lgps_civica_upm = UNSET
        else:
            report_options_lgps_civica_upm = PensionSchemeReportOptionsLgpsCivicaUpm.from_dict(_report_options_lgps_civica_upm)




        id = d.pop("id", UNSET)

        pension_scheme = cls(
            name=name,
            provider=provider,
            administrator=administrator,
            pension_rule=pension_rule,
            qualifying_scheme=qualifying_scheme,
            disable_ae_letters=disable_ae_letters,
            subtract_basic_rate_tax=subtract_basic_rate_tax,
            pay_method=pay_method,
            bank_details=bank_details,
            use_custom_pay_codes=use_custom_pay_codes,
            custom_pay_codes=custom_pay_codes,
            worker_groups=worker_groups,
            external_data_provider_id=external_data_provider_id,
            external_data_company=external_data_company,
            pay_code_type=pay_code_type,
            pay_code_set_unique_id=pay_code_set_unique_id,
            payment_date_rule=payment_date_rule,
            payment_date_day_of_week=payment_date_day_of_week,
            payment_date_day_of_month=payment_date_day_of_month,
            report_options_lgps_i_connect=report_options_lgps_i_connect,
            report_options_lgps_civica_upm=report_options_lgps_civica_upm,
            id=id,
        )

        return pension_scheme

