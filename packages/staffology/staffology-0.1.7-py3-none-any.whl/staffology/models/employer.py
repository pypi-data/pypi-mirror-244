from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..models.auto_enrolment_settings import AutoEnrolmentSettings
from ..models.bank_details import BankDetails
from ..models.bank_payment_instructions_csv_format import BankPaymentInstructionsCsvFormat
from ..models.employer_settings import EmployerSettings
from ..models.hmrc_details import HmrcDetails
from ..models.holiday_accrual import HolidayAccrual
from ..models.holiday_accrual_default_rate_type import HolidayAccrualDefaultRateType
from ..models.leave_settings import LeaveSettings
from ..models.pay_options import PayOptions
from ..models.pension_selection import PensionSelection
from ..models.rti_submission_settings import RtiSubmissionSettings
from ..models.tax_year import TaxYear
from ..models.umbrella_settings import UmbrellaSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="Employer")

@attr.s(auto_attribs=True)
class Employer:
    """
    Attributes:
        name (str):
        crn (Union[Unset, None, str]): Company Registration Number
        logo_url (Union[Unset, None, str]):
        alternative_id (Union[Unset, None, str]):
        bank_payments_csv_format (Union[Unset, BankPaymentInstructionsCsvFormat]):
        bacs_service_user_number (Union[Unset, None, str]):
        bacs_bureau_number (Union[Unset, None, str]):
        reject_invalid_bank_details (Union[Unset, bool]):
        bank_payments_reference_format (Union[Unset, None, str]):
        bacs_include_aeo (Union[Unset, bool]):
        bacs_include_deductions (Union[Unset, bool]):
        bacs_include_hmrc (Union[Unset, bool]):
        bacs_include_pensions (Union[Unset, bool]):
        use_tenant_rti_submission_settings (Union[Unset, bool]): If the Tenant for this employer has Bureau Features
            enabled then they can set RtiSubmissionSettings to be used across multiple employers.
            If this is set to true then those settings will be used instead of any set at the Employer level
        address (Union[Unset, Address]):
        bank_details (Union[Unset, BankDetails]):
        default_pay_options (Union[Unset, PayOptions]): This object forms the basis of the Employees payment.
        hmrc_details (Union[Unset, HmrcDetails]):
        default_pension (Union[Unset, PensionSelection]):
        rti_submission_settings (Union[Unset, RtiSubmissionSettings]):
        auto_enrolment_settings (Union[Unset, AutoEnrolmentSettings]):
        accrue_pay_code_set_unique_id (Union[Unset, None, str]):
        leave_settings (Union[Unset, LeaveSettings]):
        settings (Union[Unset, EmployerSettings]): Miscellaneous settings related to the employer that don't naturally
            belong in other models
        umbrella_settings (Union[Unset, UmbrellaSettings]):
        employee_count (Union[Unset, int]): [readonly] The number of Employees this Employer has, including CIS
            Subcontractors.
        subcontractor_count (Union[Unset, int]): [readonly] The number of CIS Subcontractors this Employer has.
        start_year (Union[Unset, TaxYear]):
        current_year (Union[Unset, TaxYear]):
        support_access_enabled (Union[Unset, bool]): If set to true then the support team can access this employer to
            help resolve
            support queries
        archived (Union[Unset, bool]): A flag to indicate whather or not the employer is Archived, ie no longer actively
            used
        can_use_bureau_features (Union[Unset, bool]):
        multi_role_enabled (Union[Unset, bool]):
        education_payroll_enabled (Union[Unset, bool]):
        back_pay_enabled (Union[Unset, bool]):
        is_opted_in_to_evc (Union[Unset, bool]): [readonly] Indicates whether or not the Employer is opted in to the
            Employee Verification Programme.
            Value can only be changed by its dedicated API end point.
        evc_id (Union[Unset, None, str]): If set then this will be used as the Employer ID sent to EVC in place of the
            standard EmployerId.
        holiday_accrual_basis (Union[Unset, HolidayAccrual]):
        holiday_accrual_default_rate_type (Union[Unset, HolidayAccrualDefaultRateType]):
        id (Union[Unset, str]): [readonly] The unique id of the object
        source_system_id (Union[Unset, None, str]): [readonly] Can only be given a value when the employer is created.
            It can then never be changed.
            Used by external systems so they can store an immutable reference
    """

    name: str
    crn: Union[Unset, None, str] = UNSET
    logo_url: Union[Unset, None, str] = UNSET
    alternative_id: Union[Unset, None, str] = UNSET
    bank_payments_csv_format: Union[Unset, BankPaymentInstructionsCsvFormat] = UNSET
    bacs_service_user_number: Union[Unset, None, str] = UNSET
    bacs_bureau_number: Union[Unset, None, str] = UNSET
    reject_invalid_bank_details: Union[Unset, bool] = UNSET
    bank_payments_reference_format: Union[Unset, None, str] = UNSET
    bacs_include_aeo: Union[Unset, bool] = UNSET
    bacs_include_deductions: Union[Unset, bool] = UNSET
    bacs_include_hmrc: Union[Unset, bool] = UNSET
    bacs_include_pensions: Union[Unset, bool] = UNSET
    use_tenant_rti_submission_settings: Union[Unset, bool] = UNSET
    address: Union[Unset, Address] = UNSET
    bank_details: Union[Unset, BankDetails] = UNSET
    default_pay_options: Union[Unset, PayOptions] = UNSET
    hmrc_details: Union[Unset, HmrcDetails] = UNSET
    default_pension: Union[Unset, PensionSelection] = UNSET
    rti_submission_settings: Union[Unset, RtiSubmissionSettings] = UNSET
    auto_enrolment_settings: Union[Unset, AutoEnrolmentSettings] = UNSET
    accrue_pay_code_set_unique_id: Union[Unset, None, str] = UNSET
    leave_settings: Union[Unset, LeaveSettings] = UNSET
    settings: Union[Unset, EmployerSettings] = UNSET
    umbrella_settings: Union[Unset, UmbrellaSettings] = UNSET
    employee_count: Union[Unset, int] = UNSET
    subcontractor_count: Union[Unset, int] = UNSET
    start_year: Union[Unset, TaxYear] = UNSET
    current_year: Union[Unset, TaxYear] = UNSET
    support_access_enabled: Union[Unset, bool] = UNSET
    archived: Union[Unset, bool] = UNSET
    can_use_bureau_features: Union[Unset, bool] = UNSET
    multi_role_enabled: Union[Unset, bool] = UNSET
    education_payroll_enabled: Union[Unset, bool] = UNSET
    back_pay_enabled: Union[Unset, bool] = UNSET
    is_opted_in_to_evc: Union[Unset, bool] = UNSET
    evc_id: Union[Unset, None, str] = UNSET
    holiday_accrual_basis: Union[Unset, HolidayAccrual] = UNSET
    holiday_accrual_default_rate_type: Union[Unset, HolidayAccrualDefaultRateType] = UNSET
    id: Union[Unset, str] = UNSET
    source_system_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        crn = self.crn
        logo_url = self.logo_url
        alternative_id = self.alternative_id
        bank_payments_csv_format: Union[Unset, str] = UNSET
        if not isinstance(self.bank_payments_csv_format, Unset):
            bank_payments_csv_format = self.bank_payments_csv_format.value

        bacs_service_user_number = self.bacs_service_user_number
        bacs_bureau_number = self.bacs_bureau_number
        reject_invalid_bank_details = self.reject_invalid_bank_details
        bank_payments_reference_format = self.bank_payments_reference_format
        bacs_include_aeo = self.bacs_include_aeo
        bacs_include_deductions = self.bacs_include_deductions
        bacs_include_hmrc = self.bacs_include_hmrc
        bacs_include_pensions = self.bacs_include_pensions
        use_tenant_rti_submission_settings = self.use_tenant_rti_submission_settings
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        default_pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_pay_options, Unset):
            default_pay_options = self.default_pay_options.to_dict()

        hmrc_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hmrc_details, Unset):
            hmrc_details = self.hmrc_details.to_dict()

        default_pension: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_pension, Unset):
            default_pension = self.default_pension.to_dict()

        rti_submission_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rti_submission_settings, Unset):
            rti_submission_settings = self.rti_submission_settings.to_dict()

        auto_enrolment_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_enrolment_settings, Unset):
            auto_enrolment_settings = self.auto_enrolment_settings.to_dict()

        accrue_pay_code_set_unique_id = self.accrue_pay_code_set_unique_id
        leave_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leave_settings, Unset):
            leave_settings = self.leave_settings.to_dict()

        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        umbrella_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.umbrella_settings, Unset):
            umbrella_settings = self.umbrella_settings.to_dict()

        employee_count = self.employee_count
        subcontractor_count = self.subcontractor_count
        start_year: Union[Unset, str] = UNSET
        if not isinstance(self.start_year, Unset):
            start_year = self.start_year.value

        current_year: Union[Unset, str] = UNSET
        if not isinstance(self.current_year, Unset):
            current_year = self.current_year.value

        support_access_enabled = self.support_access_enabled
        archived = self.archived
        can_use_bureau_features = self.can_use_bureau_features
        multi_role_enabled = self.multi_role_enabled
        education_payroll_enabled = self.education_payroll_enabled
        back_pay_enabled = self.back_pay_enabled
        is_opted_in_to_evc = self.is_opted_in_to_evc
        evc_id = self.evc_id
        holiday_accrual_basis: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_accrual_basis, Unset):
            holiday_accrual_basis = self.holiday_accrual_basis.value

        holiday_accrual_default_rate_type: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_accrual_default_rate_type, Unset):
            holiday_accrual_default_rate_type = self.holiday_accrual_default_rate_type.value

        id = self.id
        source_system_id = self.source_system_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if crn is not UNSET:
            field_dict["crn"] = crn
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if alternative_id is not UNSET:
            field_dict["alternativeId"] = alternative_id
        if bank_payments_csv_format is not UNSET:
            field_dict["bankPaymentsCsvFormat"] = bank_payments_csv_format
        if bacs_service_user_number is not UNSET:
            field_dict["bacsServiceUserNumber"] = bacs_service_user_number
        if bacs_bureau_number is not UNSET:
            field_dict["bacsBureauNumber"] = bacs_bureau_number
        if reject_invalid_bank_details is not UNSET:
            field_dict["rejectInvalidBankDetails"] = reject_invalid_bank_details
        if bank_payments_reference_format is not UNSET:
            field_dict["bankPaymentsReferenceFormat"] = bank_payments_reference_format
        if bacs_include_aeo is not UNSET:
            field_dict["bacsIncludeAEO"] = bacs_include_aeo
        if bacs_include_deductions is not UNSET:
            field_dict["bacsIncludeDeductions"] = bacs_include_deductions
        if bacs_include_hmrc is not UNSET:
            field_dict["bacsIncludeHmrc"] = bacs_include_hmrc
        if bacs_include_pensions is not UNSET:
            field_dict["bacsIncludePensions"] = bacs_include_pensions
        if use_tenant_rti_submission_settings is not UNSET:
            field_dict["useTenantRtiSubmissionSettings"] = use_tenant_rti_submission_settings
        if address is not UNSET:
            field_dict["address"] = address
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if default_pay_options is not UNSET:
            field_dict["defaultPayOptions"] = default_pay_options
        if hmrc_details is not UNSET:
            field_dict["hmrcDetails"] = hmrc_details
        if default_pension is not UNSET:
            field_dict["defaultPension"] = default_pension
        if rti_submission_settings is not UNSET:
            field_dict["rtiSubmissionSettings"] = rti_submission_settings
        if auto_enrolment_settings is not UNSET:
            field_dict["autoEnrolmentSettings"] = auto_enrolment_settings
        if accrue_pay_code_set_unique_id is not UNSET:
            field_dict["accruePayCodeSetUniqueId"] = accrue_pay_code_set_unique_id
        if leave_settings is not UNSET:
            field_dict["leaveSettings"] = leave_settings
        if settings is not UNSET:
            field_dict["settings"] = settings
        if umbrella_settings is not UNSET:
            field_dict["umbrellaSettings"] = umbrella_settings
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if subcontractor_count is not UNSET:
            field_dict["subcontractorCount"] = subcontractor_count
        if start_year is not UNSET:
            field_dict["startYear"] = start_year
        if current_year is not UNSET:
            field_dict["currentYear"] = current_year
        if support_access_enabled is not UNSET:
            field_dict["supportAccessEnabled"] = support_access_enabled
        if archived is not UNSET:
            field_dict["archived"] = archived
        if can_use_bureau_features is not UNSET:
            field_dict["canUseBureauFeatures"] = can_use_bureau_features
        if multi_role_enabled is not UNSET:
            field_dict["multiRoleEnabled"] = multi_role_enabled
        if education_payroll_enabled is not UNSET:
            field_dict["educationPayrollEnabled"] = education_payroll_enabled
        if back_pay_enabled is not UNSET:
            field_dict["backPayEnabled"] = back_pay_enabled
        if is_opted_in_to_evc is not UNSET:
            field_dict["isOptedInToEvc"] = is_opted_in_to_evc
        if evc_id is not UNSET:
            field_dict["evcId"] = evc_id
        if holiday_accrual_basis is not UNSET:
            field_dict["holidayAccrualBasis"] = holiday_accrual_basis
        if holiday_accrual_default_rate_type is not UNSET:
            field_dict["holidayAccrualDefaultRateType"] = holiday_accrual_default_rate_type
        if id is not UNSET:
            field_dict["id"] = id
        if source_system_id is not UNSET:
            field_dict["sourceSystemId"] = source_system_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        crn = d.pop("crn", UNSET)

        logo_url = d.pop("logoUrl", UNSET)

        alternative_id = d.pop("alternativeId", UNSET)

        _bank_payments_csv_format = d.pop("bankPaymentsCsvFormat", UNSET)
        bank_payments_csv_format: Union[Unset, BankPaymentInstructionsCsvFormat]
        if isinstance(_bank_payments_csv_format,  Unset):
            bank_payments_csv_format = UNSET
        else:
            bank_payments_csv_format = BankPaymentInstructionsCsvFormat(_bank_payments_csv_format)




        bacs_service_user_number = d.pop("bacsServiceUserNumber", UNSET)

        bacs_bureau_number = d.pop("bacsBureauNumber", UNSET)

        reject_invalid_bank_details = d.pop("rejectInvalidBankDetails", UNSET)

        bank_payments_reference_format = d.pop("bankPaymentsReferenceFormat", UNSET)

        bacs_include_aeo = d.pop("bacsIncludeAEO", UNSET)

        bacs_include_deductions = d.pop("bacsIncludeDeductions", UNSET)

        bacs_include_hmrc = d.pop("bacsIncludeHmrc", UNSET)

        bacs_include_pensions = d.pop("bacsIncludePensions", UNSET)

        use_tenant_rti_submission_settings = d.pop("useTenantRtiSubmissionSettings", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address,  Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)




        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details,  Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)




        _default_pay_options = d.pop("defaultPayOptions", UNSET)
        default_pay_options: Union[Unset, PayOptions]
        if isinstance(_default_pay_options,  Unset):
            default_pay_options = UNSET
        else:
            default_pay_options = PayOptions.from_dict(_default_pay_options)




        _hmrc_details = d.pop("hmrcDetails", UNSET)
        hmrc_details: Union[Unset, HmrcDetails]
        if isinstance(_hmrc_details,  Unset):
            hmrc_details = UNSET
        else:
            hmrc_details = HmrcDetails.from_dict(_hmrc_details)




        _default_pension = d.pop("defaultPension", UNSET)
        default_pension: Union[Unset, PensionSelection]
        if isinstance(_default_pension,  Unset):
            default_pension = UNSET
        else:
            default_pension = PensionSelection.from_dict(_default_pension)




        _rti_submission_settings = d.pop("rtiSubmissionSettings", UNSET)
        rti_submission_settings: Union[Unset, RtiSubmissionSettings]
        if isinstance(_rti_submission_settings,  Unset):
            rti_submission_settings = UNSET
        else:
            rti_submission_settings = RtiSubmissionSettings.from_dict(_rti_submission_settings)




        _auto_enrolment_settings = d.pop("autoEnrolmentSettings", UNSET)
        auto_enrolment_settings: Union[Unset, AutoEnrolmentSettings]
        if isinstance(_auto_enrolment_settings,  Unset):
            auto_enrolment_settings = UNSET
        else:
            auto_enrolment_settings = AutoEnrolmentSettings.from_dict(_auto_enrolment_settings)




        accrue_pay_code_set_unique_id = d.pop("accruePayCodeSetUniqueId", UNSET)

        _leave_settings = d.pop("leaveSettings", UNSET)
        leave_settings: Union[Unset, LeaveSettings]
        if isinstance(_leave_settings,  Unset):
            leave_settings = UNSET
        else:
            leave_settings = LeaveSettings.from_dict(_leave_settings)




        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, EmployerSettings]
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = EmployerSettings.from_dict(_settings)




        _umbrella_settings = d.pop("umbrellaSettings", UNSET)
        umbrella_settings: Union[Unset, UmbrellaSettings]
        if isinstance(_umbrella_settings,  Unset):
            umbrella_settings = UNSET
        else:
            umbrella_settings = UmbrellaSettings.from_dict(_umbrella_settings)




        employee_count = d.pop("employeeCount", UNSET)

        subcontractor_count = d.pop("subcontractorCount", UNSET)

        _start_year = d.pop("startYear", UNSET)
        start_year: Union[Unset, TaxYear]
        if isinstance(_start_year,  Unset):
            start_year = UNSET
        else:
            start_year = TaxYear(_start_year)




        _current_year = d.pop("currentYear", UNSET)
        current_year: Union[Unset, TaxYear]
        if isinstance(_current_year,  Unset):
            current_year = UNSET
        else:
            current_year = TaxYear(_current_year)




        support_access_enabled = d.pop("supportAccessEnabled", UNSET)

        archived = d.pop("archived", UNSET)

        can_use_bureau_features = d.pop("canUseBureauFeatures", UNSET)

        multi_role_enabled = d.pop("multiRoleEnabled", UNSET)

        education_payroll_enabled = d.pop("educationPayrollEnabled", UNSET)

        back_pay_enabled = d.pop("backPayEnabled", UNSET)

        is_opted_in_to_evc = d.pop("isOptedInToEvc", UNSET)

        evc_id = d.pop("evcId", UNSET)

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




        id = d.pop("id", UNSET)

        source_system_id = d.pop("sourceSystemId", UNSET)

        employer = cls(
            name=name,
            crn=crn,
            logo_url=logo_url,
            alternative_id=alternative_id,
            bank_payments_csv_format=bank_payments_csv_format,
            bacs_service_user_number=bacs_service_user_number,
            bacs_bureau_number=bacs_bureau_number,
            reject_invalid_bank_details=reject_invalid_bank_details,
            bank_payments_reference_format=bank_payments_reference_format,
            bacs_include_aeo=bacs_include_aeo,
            bacs_include_deductions=bacs_include_deductions,
            bacs_include_hmrc=bacs_include_hmrc,
            bacs_include_pensions=bacs_include_pensions,
            use_tenant_rti_submission_settings=use_tenant_rti_submission_settings,
            address=address,
            bank_details=bank_details,
            default_pay_options=default_pay_options,
            hmrc_details=hmrc_details,
            default_pension=default_pension,
            rti_submission_settings=rti_submission_settings,
            auto_enrolment_settings=auto_enrolment_settings,
            accrue_pay_code_set_unique_id=accrue_pay_code_set_unique_id,
            leave_settings=leave_settings,
            settings=settings,
            umbrella_settings=umbrella_settings,
            employee_count=employee_count,
            subcontractor_count=subcontractor_count,
            start_year=start_year,
            current_year=current_year,
            support_access_enabled=support_access_enabled,
            archived=archived,
            can_use_bureau_features=can_use_bureau_features,
            multi_role_enabled=multi_role_enabled,
            education_payroll_enabled=education_payroll_enabled,
            back_pay_enabled=back_pay_enabled,
            is_opted_in_to_evc=is_opted_in_to_evc,
            evc_id=evc_id,
            holiday_accrual_basis=holiday_accrual_basis,
            holiday_accrual_default_rate_type=holiday_accrual_default_rate_type,
            id=id,
            source_system_id=source_system_id,
        )

        return employer

