from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_large_file_storage_config_response_200_type import GetLargeFileStorageConfigResponse200Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetLargeFileStorageConfigResponse200")


@_attrs_define
class GetLargeFileStorageConfigResponse200:
    """
    Attributes:
        type (Union[Unset, GetLargeFileStorageConfigResponse200Type]):
        s3_resource_path (Union[Unset, str]):
    """

    type: Union[Unset, GetLargeFileStorageConfigResponse200Type] = UNSET
    s3_resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        s3_resource_path = self.s3_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if s3_resource_path is not UNSET:
            field_dict["s3_resource_path"] = s3_resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, GetLargeFileStorageConfigResponse200Type]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetLargeFileStorageConfigResponse200Type(_type)

        s3_resource_path = d.pop("s3_resource_path", UNSET)

        get_large_file_storage_config_response_200 = cls(
            type=type,
            s3_resource_path=s3_resource_path,
        )

        get_large_file_storage_config_response_200.additional_properties = d
        return get_large_file_storage_config_response_200

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
