import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.processing_note_status import ProcessingNoteStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessingNote")

@attr.s(auto_attribs=True)
class ProcessingNote:
    """
    Attributes:
        note (str):
        pay_run_entry_id (Union[Unset, None, str]): The Id of the payrunEntry this ProcessingNote relates to, if any
        user (Union[Unset, Item]):
        pay_run (Union[Unset, Item]):
        date (Union[Unset, datetime.date]):
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        status (Union[Unset, ProcessingNoteStatus]):
        updated_by_name (Union[Unset, None, str]): Name of the user who was last to update the record
        completed_date (Union[Unset, None, datetime.date]): UpdatedDate is assigned to this to get around the base
            implementation of UpdatedDate having [JsonIgnore] tag
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    note: str
    pay_run_entry_id: Union[Unset, None, str] = UNSET
    user: Union[Unset, Item] = UNSET
    pay_run: Union[Unset, Item] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    status: Union[Unset, ProcessingNoteStatus] = UNSET
    updated_by_name: Union[Unset, None, str] = UNSET
    completed_date: Union[Unset, None, datetime.date] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        note = self.note
        pay_run_entry_id = self.pay_run_entry_id
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        pay_run: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_run, Unset):
            pay_run = self.pay_run.to_dict()

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        document_count = self.document_count
        documents: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            if self.documents is None:
                documents = None
            else:
                documents = []
                for documents_item_data in self.documents:
                    documents_item = documents_item_data.to_dict()

                    documents.append(documents_item)




        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        updated_by_name = self.updated_by_name
        completed_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.completed_date, Unset):
            completed_date = self.completed_date.isoformat() if self.completed_date else None

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "note": note,
        })
        if pay_run_entry_id is not UNSET:
            field_dict["payRunEntryId"] = pay_run_entry_id
        if user is not UNSET:
            field_dict["user"] = user
        if pay_run is not UNSET:
            field_dict["payRun"] = pay_run
        if date is not UNSET:
            field_dict["date"] = date
        if document_count is not UNSET:
            field_dict["documentCount"] = document_count
        if documents is not UNSET:
            field_dict["documents"] = documents
        if status is not UNSET:
            field_dict["status"] = status
        if updated_by_name is not UNSET:
            field_dict["updatedByName"] = updated_by_name
        if completed_date is not UNSET:
            field_dict["completedDate"] = completed_date
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        note = d.pop("note")

        pay_run_entry_id = d.pop("payRunEntryId", UNSET)

        _user = d.pop("user", UNSET)
        user: Union[Unset, Item]
        if isinstance(_user,  Unset):
            user = UNSET
        else:
            user = Item.from_dict(_user)




        _pay_run = d.pop("payRun", UNSET)
        pay_run: Union[Unset, Item]
        if isinstance(_pay_run,  Unset):
            pay_run = UNSET
        else:
            pay_run = Item.from_dict(_pay_run)




        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date,  Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()




        document_count = d.pop("documentCount", UNSET)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in (_documents or []):
            documents_item = Item.from_dict(documents_item_data)



            documents.append(documents_item)


        _status = d.pop("status", UNSET)
        status: Union[Unset, ProcessingNoteStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = ProcessingNoteStatus(_status)




        updated_by_name = d.pop("updatedByName", UNSET)

        _completed_date = d.pop("completedDate", UNSET)
        completed_date: Union[Unset, None, datetime.date]
        if _completed_date is None:
            completed_date = None
        elif isinstance(_completed_date,  Unset):
            completed_date = UNSET
        else:
            completed_date = isoparse(_completed_date).date()




        id = d.pop("id", UNSET)

        processing_note = cls(
            note=note,
            pay_run_entry_id=pay_run_entry_id,
            user=user,
            pay_run=pay_run,
            date=date,
            document_count=document_count,
            documents=documents,
            status=status,
            updated_by_name=updated_by_name,
            completed_date=completed_date,
            id=id,
        )

        return processing_note

