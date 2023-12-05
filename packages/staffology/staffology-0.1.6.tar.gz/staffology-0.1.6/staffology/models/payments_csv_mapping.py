from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pay_basis import PayBasis
from ..models.payments_csv_mapping_column import PaymentsCsvMappingColumn
from ..models.payments_csv_mapping_type import PaymentsCsvMappingType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentsCsvMapping")

@attr.s(auto_attribs=True)
class PaymentsCsvMapping:
    """This model is used to save CSV mappings for importing of payments.
It probably has very little practical use outside of our own UI

    Attributes:
        name (str):
        type (Union[Unset, PaymentsCsvMappingType]):
        import_behaviour (Union[Unset, int]):
        pay_basis (Union[Unset, PayBasis]):
        has_header (Union[Unset, bool]):
        payroll_code_index (Union[Unset, int]):
        employer_id_index (Union[Unset, int]):
        role_reference_index (Union[Unset, int]):
        pay_amount_index (Union[Unset, int]):
        pay_amount_multiplier_index (Union[Unset, int]):
        note_index (Union[Unset, int]):
        pay_code_index (Union[Unset, int]):
        has_payline_costing (Union[Unset, bool]):
        department_index (Union[Unset, int]):
        cost_centre_index (Union[Unset, int]):
        effective_from_index (Union[Unset, int]):
        effective_to_index (Union[Unset, int]):
        is_automatic_back_pay_index (Union[Unset, int]):
        ignore_initial_back_pay_index (Union[Unset, int]):
        contributes_to_basic_pay_index (Union[Unset, int]):
        auto_adjust_for_leave_index (Union[Unset, int]):
        columns (Union[Unset, None, List[PaymentsCsvMappingColumn]]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    type: Union[Unset, PaymentsCsvMappingType] = UNSET
    import_behaviour: Union[Unset, int] = UNSET
    pay_basis: Union[Unset, PayBasis] = UNSET
    has_header: Union[Unset, bool] = UNSET
    payroll_code_index: Union[Unset, int] = UNSET
    employer_id_index: Union[Unset, int] = UNSET
    role_reference_index: Union[Unset, int] = UNSET
    pay_amount_index: Union[Unset, int] = UNSET
    pay_amount_multiplier_index: Union[Unset, int] = UNSET
    note_index: Union[Unset, int] = UNSET
    pay_code_index: Union[Unset, int] = UNSET
    has_payline_costing: Union[Unset, bool] = UNSET
    department_index: Union[Unset, int] = UNSET
    cost_centre_index: Union[Unset, int] = UNSET
    effective_from_index: Union[Unset, int] = UNSET
    effective_to_index: Union[Unset, int] = UNSET
    is_automatic_back_pay_index: Union[Unset, int] = UNSET
    ignore_initial_back_pay_index: Union[Unset, int] = UNSET
    contributes_to_basic_pay_index: Union[Unset, int] = UNSET
    auto_adjust_for_leave_index: Union[Unset, int] = UNSET
    columns: Union[Unset, None, List[PaymentsCsvMappingColumn]] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        import_behaviour = self.import_behaviour
        pay_basis: Union[Unset, str] = UNSET
        if not isinstance(self.pay_basis, Unset):
            pay_basis = self.pay_basis.value

        has_header = self.has_header
        payroll_code_index = self.payroll_code_index
        employer_id_index = self.employer_id_index
        role_reference_index = self.role_reference_index
        pay_amount_index = self.pay_amount_index
        pay_amount_multiplier_index = self.pay_amount_multiplier_index
        note_index = self.note_index
        pay_code_index = self.pay_code_index
        has_payline_costing = self.has_payline_costing
        department_index = self.department_index
        cost_centre_index = self.cost_centre_index
        effective_from_index = self.effective_from_index
        effective_to_index = self.effective_to_index
        is_automatic_back_pay_index = self.is_automatic_back_pay_index
        ignore_initial_back_pay_index = self.ignore_initial_back_pay_index
        contributes_to_basic_pay_index = self.contributes_to_basic_pay_index
        auto_adjust_for_leave_index = self.auto_adjust_for_leave_index
        columns: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            if self.columns is None:
                columns = None
            else:
                columns = []
                for columns_item_data in self.columns:
                    columns_item = columns_item_data.to_dict()

                    columns.append(columns_item)




        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if type is not UNSET:
            field_dict["type"] = type
        if import_behaviour is not UNSET:
            field_dict["importBehaviour"] = import_behaviour
        if pay_basis is not UNSET:
            field_dict["payBasis"] = pay_basis
        if has_header is not UNSET:
            field_dict["hasHeader"] = has_header
        if payroll_code_index is not UNSET:
            field_dict["payrollCodeIndex"] = payroll_code_index
        if employer_id_index is not UNSET:
            field_dict["employerIdIndex"] = employer_id_index
        if role_reference_index is not UNSET:
            field_dict["roleReferenceIndex"] = role_reference_index
        if pay_amount_index is not UNSET:
            field_dict["payAmountIndex"] = pay_amount_index
        if pay_amount_multiplier_index is not UNSET:
            field_dict["payAmountMultiplierIndex"] = pay_amount_multiplier_index
        if note_index is not UNSET:
            field_dict["noteIndex"] = note_index
        if pay_code_index is not UNSET:
            field_dict["payCodeIndex"] = pay_code_index
        if has_payline_costing is not UNSET:
            field_dict["hasPaylineCosting"] = has_payline_costing
        if department_index is not UNSET:
            field_dict["departmentIndex"] = department_index
        if cost_centre_index is not UNSET:
            field_dict["costCentreIndex"] = cost_centre_index
        if effective_from_index is not UNSET:
            field_dict["effectiveFromIndex"] = effective_from_index
        if effective_to_index is not UNSET:
            field_dict["effectiveToIndex"] = effective_to_index
        if is_automatic_back_pay_index is not UNSET:
            field_dict["isAutomaticBackPayIndex"] = is_automatic_back_pay_index
        if ignore_initial_back_pay_index is not UNSET:
            field_dict["ignoreInitialBackPayIndex"] = ignore_initial_back_pay_index
        if contributes_to_basic_pay_index is not UNSET:
            field_dict["contributesToBasicPayIndex"] = contributes_to_basic_pay_index
        if auto_adjust_for_leave_index is not UNSET:
            field_dict["autoAdjustForLeaveIndex"] = auto_adjust_for_leave_index
        if columns is not UNSET:
            field_dict["columns"] = columns
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _type = d.pop("type", UNSET)
        type: Union[Unset, PaymentsCsvMappingType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = PaymentsCsvMappingType(_type)




        import_behaviour = d.pop("importBehaviour", UNSET)

        _pay_basis = d.pop("payBasis", UNSET)
        pay_basis: Union[Unset, PayBasis]
        if isinstance(_pay_basis,  Unset):
            pay_basis = UNSET
        else:
            pay_basis = PayBasis(_pay_basis)




        has_header = d.pop("hasHeader", UNSET)

        payroll_code_index = d.pop("payrollCodeIndex", UNSET)

        employer_id_index = d.pop("employerIdIndex", UNSET)

        role_reference_index = d.pop("roleReferenceIndex", UNSET)

        pay_amount_index = d.pop("payAmountIndex", UNSET)

        pay_amount_multiplier_index = d.pop("payAmountMultiplierIndex", UNSET)

        note_index = d.pop("noteIndex", UNSET)

        pay_code_index = d.pop("payCodeIndex", UNSET)

        has_payline_costing = d.pop("hasPaylineCosting", UNSET)

        department_index = d.pop("departmentIndex", UNSET)

        cost_centre_index = d.pop("costCentreIndex", UNSET)

        effective_from_index = d.pop("effectiveFromIndex", UNSET)

        effective_to_index = d.pop("effectiveToIndex", UNSET)

        is_automatic_back_pay_index = d.pop("isAutomaticBackPayIndex", UNSET)

        ignore_initial_back_pay_index = d.pop("ignoreInitialBackPayIndex", UNSET)

        contributes_to_basic_pay_index = d.pop("contributesToBasicPayIndex", UNSET)

        auto_adjust_for_leave_index = d.pop("autoAdjustForLeaveIndex", UNSET)

        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in (_columns or []):
            columns_item = PaymentsCsvMappingColumn.from_dict(columns_item_data)



            columns.append(columns_item)


        id = d.pop("id", UNSET)

        payments_csv_mapping = cls(
            name=name,
            type=type,
            import_behaviour=import_behaviour,
            pay_basis=pay_basis,
            has_header=has_header,
            payroll_code_index=payroll_code_index,
            employer_id_index=employer_id_index,
            role_reference_index=role_reference_index,
            pay_amount_index=pay_amount_index,
            pay_amount_multiplier_index=pay_amount_multiplier_index,
            note_index=note_index,
            pay_code_index=pay_code_index,
            has_payline_costing=has_payline_costing,
            department_index=department_index,
            cost_centre_index=cost_centre_index,
            effective_from_index=effective_from_index,
            effective_to_index=effective_to_index,
            is_automatic_back_pay_index=is_automatic_back_pay_index,
            ignore_initial_back_pay_index=ignore_initial_back_pay_index,
            contributes_to_basic_pay_index=contributes_to_basic_pay_index,
            auto_adjust_for_leave_index=auto_adjust_for_leave_index,
            columns=columns,
            id=id,
        )

        return payments_csv_mapping

