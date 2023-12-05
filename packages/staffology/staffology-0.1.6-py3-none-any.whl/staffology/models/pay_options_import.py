import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.pay_basis import PayBasis
from ..models.pay_line import PayLine
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayOptionsImport")

@attr.s(auto_attribs=True)
class PayOptionsImport:
    """This object is used to import payment information for a payrun entry

    Attributes:
        employer_identifier (Union[Unset, None, str]): Optional. But if one entry has it then all must.
            Allows you to import to multiple employers by specifying the Employers AlternativeIdentifier
        payroll_code (Union[Unset, None, str]): The payroll code of the employee to update
        pay_amount (Union[Unset, float]): The amount the Employee is regularly paid each period
        basis (Union[Unset, PayBasis]):
        pay_code (Union[Unset, None, str]): If you want to override the PayCode used for the Basic Pay then set the code
            here, otherwise leave this blank and the default will be used.
        role_reference (Union[Unset, None, str]): This is the unique reference of the Role that the employee is assigned
            to.
        pay_amount_multiplier (Union[Unset, float]): This property is irrelevant if the basis is Monthly.
            But if the basis is Daily or Hourly then this property sets how many days/hours the employee should be paid for
            in the period.
        note (Union[Unset, None, str]): Any note that you'd like to appear on the payslip
        tags (Union[Unset, None, List[str]]):
        is_net_to_gross (Union[Unset, bool]):
        department (Union[Unset, None, str]): Any Department that you'd like to appear on the payslip
        cost_centre (Union[Unset, None, str]): Any CostCentre that you'd like to appear on the payslip
        lines (Union[Unset, None, List[PayLine]]):
        effective_from (Union[Unset, None, datetime.date]): EffectiveFrom date for imported pay lines
        effective_to (Union[Unset, None, datetime.date]): EffectiveTo date for imported pay lines
        is_automatic_back_pay (Union[Unset, bool]): IsAutomaticBackPay for imported pay lines
        ignore_initial_back_pay (Union[Unset, bool]): IgnoreInitialBackPay for imported pay lines
        contributes_to_basic_pay (Union[Unset, bool]): ContributesToBasicPay for imported pay lines
        auto_adjust_for_leave (Union[Unset, bool]): AutoAdjustForLeave for imported pay lines
    """

    employer_identifier: Union[Unset, None, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    pay_amount: Union[Unset, float] = UNSET
    basis: Union[Unset, PayBasis] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    role_reference: Union[Unset, None, str] = UNSET
    pay_amount_multiplier: Union[Unset, float] = UNSET
    note: Union[Unset, None, str] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    is_net_to_gross: Union[Unset, bool] = UNSET
    department: Union[Unset, None, str] = UNSET
    cost_centre: Union[Unset, None, str] = UNSET
    lines: Union[Unset, None, List[PayLine]] = UNSET
    effective_from: Union[Unset, None, datetime.date] = UNSET
    effective_to: Union[Unset, None, datetime.date] = UNSET
    is_automatic_back_pay: Union[Unset, bool] = UNSET
    ignore_initial_back_pay: Union[Unset, bool] = UNSET
    contributes_to_basic_pay: Union[Unset, bool] = UNSET
    auto_adjust_for_leave: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        employer_identifier = self.employer_identifier
        payroll_code = self.payroll_code
        pay_amount = self.pay_amount
        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        pay_code = self.pay_code
        role_reference = self.role_reference
        pay_amount_multiplier = self.pay_amount_multiplier
        note = self.note
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags




        is_net_to_gross = self.is_net_to_gross
        department = self.department
        cost_centre = self.cost_centre
        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)




        effective_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.effective_from, Unset):
            effective_from = self.effective_from.isoformat() if self.effective_from else None

        effective_to: Union[Unset, None, str] = UNSET
        if not isinstance(self.effective_to, Unset):
            effective_to = self.effective_to.isoformat() if self.effective_to else None

        is_automatic_back_pay = self.is_automatic_back_pay
        ignore_initial_back_pay = self.ignore_initial_back_pay
        contributes_to_basic_pay = self.contributes_to_basic_pay
        auto_adjust_for_leave = self.auto_adjust_for_leave

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if employer_identifier is not UNSET:
            field_dict["employerIdentifier"] = employer_identifier
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if pay_amount is not UNSET:
            field_dict["payAmount"] = pay_amount
        if basis is not UNSET:
            field_dict["basis"] = basis
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if role_reference is not UNSET:
            field_dict["roleReference"] = role_reference
        if pay_amount_multiplier is not UNSET:
            field_dict["payAmountMultiplier"] = pay_amount_multiplier
        if note is not UNSET:
            field_dict["note"] = note
        if tags is not UNSET:
            field_dict["tags"] = tags
        if is_net_to_gross is not UNSET:
            field_dict["isNetToGross"] = is_net_to_gross
        if department is not UNSET:
            field_dict["department"] = department
        if cost_centre is not UNSET:
            field_dict["costCentre"] = cost_centre
        if lines is not UNSET:
            field_dict["lines"] = lines
        if effective_from is not UNSET:
            field_dict["effectiveFrom"] = effective_from
        if effective_to is not UNSET:
            field_dict["effectiveTo"] = effective_to
        if is_automatic_back_pay is not UNSET:
            field_dict["isAutomaticBackPay"] = is_automatic_back_pay
        if ignore_initial_back_pay is not UNSET:
            field_dict["ignoreInitialBackPay"] = ignore_initial_back_pay
        if contributes_to_basic_pay is not UNSET:
            field_dict["contributesToBasicPay"] = contributes_to_basic_pay
        if auto_adjust_for_leave is not UNSET:
            field_dict["autoAdjustForLeave"] = auto_adjust_for_leave

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_identifier = d.pop("employerIdentifier", UNSET)

        payroll_code = d.pop("payrollCode", UNSET)

        pay_amount = d.pop("payAmount", UNSET)

        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, PayBasis]
        if isinstance(_basis,  Unset):
            basis = UNSET
        else:
            basis = PayBasis(_basis)




        pay_code = d.pop("payCode", UNSET)

        role_reference = d.pop("roleReference", UNSET)

        pay_amount_multiplier = d.pop("payAmountMultiplier", UNSET)

        note = d.pop("note", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))


        is_net_to_gross = d.pop("isNetToGross", UNSET)

        department = d.pop("department", UNSET)

        cost_centre = d.pop("costCentre", UNSET)

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in (_lines or []):
            lines_item = PayLine.from_dict(lines_item_data)



            lines.append(lines_item)


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




        is_automatic_back_pay = d.pop("isAutomaticBackPay", UNSET)

        ignore_initial_back_pay = d.pop("ignoreInitialBackPay", UNSET)

        contributes_to_basic_pay = d.pop("contributesToBasicPay", UNSET)

        auto_adjust_for_leave = d.pop("autoAdjustForLeave", UNSET)

        pay_options_import = cls(
            employer_identifier=employer_identifier,
            payroll_code=payroll_code,
            pay_amount=pay_amount,
            basis=basis,
            pay_code=pay_code,
            role_reference=role_reference,
            pay_amount_multiplier=pay_amount_multiplier,
            note=note,
            tags=tags,
            is_net_to_gross=is_net_to_gross,
            department=department,
            cost_centre=cost_centre,
            lines=lines,
            effective_from=effective_from,
            effective_to=effective_to,
            is_automatic_back_pay=is_automatic_back_pay,
            ignore_initial_back_pay=ignore_initial_back_pay,
            contributes_to_basic_pay=contributes_to_basic_pay,
            auto_adjust_for_leave=auto_adjust_for_leave,
        )

        return pay_options_import

