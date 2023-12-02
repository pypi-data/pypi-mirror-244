import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataResponse200ResponseResultItem")


@_attrs_define
class MetadataResponse200ResponseResultItem:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        data_source (Union[Unset, str]):
        data_collection (Union[Unset, str]):
        description (Union[Unset, str]):
        maxvalue (Union[Unset, float]):
        minvalue (Union[Unset, float]):
        startdate (Union[Unset, datetime.datetime]):
        enddate (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    data_source: Union[Unset, str] = UNSET
    data_collection: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    maxvalue: Union[Unset, float] = UNSET
    minvalue: Union[Unset, float] = UNSET
    startdate: Union[Unset, datetime.datetime] = UNSET
    enddate: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        data_source = self.data_source
        data_collection = self.data_collection
        description = self.description
        maxvalue = self.maxvalue
        minvalue = self.minvalue
        startdate: Union[Unset, str] = UNSET
        if not isinstance(self.startdate, Unset):
            startdate = self.startdate.isoformat()

        enddate: Union[Unset, str] = UNSET
        if not isinstance(self.enddate, Unset):
            enddate = self.enddate.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if data_source is not UNSET:
            field_dict["data_source"] = data_source
        if data_collection is not UNSET:
            field_dict["data_collection"] = data_collection
        if description is not UNSET:
            field_dict["description"] = description
        if maxvalue is not UNSET:
            field_dict["maxvalue"] = maxvalue
        if minvalue is not UNSET:
            field_dict["minvalue"] = minvalue
        if startdate is not UNSET:
            field_dict["startdate"] = startdate
        if enddate is not UNSET:
            field_dict["enddate"] = enddate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        data_source = d.pop("data_source", UNSET)

        data_collection = d.pop("data_collection", UNSET)

        description = d.pop("description", UNSET)

        maxvalue = d.pop("maxvalue", UNSET)

        minvalue = d.pop("minvalue", UNSET)

        _startdate = d.pop("startdate", UNSET)
        startdate: Union[Unset, datetime.datetime]
        if isinstance(_startdate, Unset):
            startdate = UNSET
        else:
            startdate = isoparse(_startdate)

        _enddate = d.pop("enddate", UNSET)
        enddate: Union[Unset, datetime.datetime]
        if isinstance(_enddate, Unset):
            enddate = UNSET
        else:
            enddate = isoparse(_enddate)

        metadata_response_200_response_result_item = cls(
            id=id,
            name=name,
            data_source=data_source,
            data_collection=data_collection,
            description=description,
            maxvalue=maxvalue,
            minvalue=minvalue,
            startdate=startdate,
            enddate=enddate,
        )

        metadata_response_200_response_result_item.additional_properties = d
        return metadata_response_200_response_result_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
