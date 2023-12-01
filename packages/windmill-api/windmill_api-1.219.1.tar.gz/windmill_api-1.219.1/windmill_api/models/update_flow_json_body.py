from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_flow_json_body_schema import UpdateFlowJsonBodySchema
    from ..models.update_flow_json_body_value import UpdateFlowJsonBodyValue


T = TypeVar("T", bound="UpdateFlowJsonBody")


@_attrs_define
class UpdateFlowJsonBody:
    """
    Attributes:
        summary (str):
        value (UpdateFlowJsonBodyValue):
        path (str):
        description (Union[Unset, str]):
        schema (Union[Unset, UpdateFlowJsonBodySchema]):
        tag (Union[Unset, str]):
        ws_error_handler_muted (Union[Unset, bool]):
        priority (Union[Unset, int]):
        dedicated_worker (Union[Unset, bool]):
    """

    summary: str
    value: "UpdateFlowJsonBodyValue"
    path: str
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "UpdateFlowJsonBodySchema"] = UNSET
    tag: Union[Unset, str] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        value = self.value.to_dict()

        path = self.path
        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        tag = self.tag
        ws_error_handler_muted = self.ws_error_handler_muted
        priority = self.priority
        dedicated_worker = self.dedicated_worker

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "value": value,
                "path": path,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema
        if tag is not UNSET:
            field_dict["tag"] = tag
        if ws_error_handler_muted is not UNSET:
            field_dict["ws_error_handler_muted"] = ws_error_handler_muted
        if priority is not UNSET:
            field_dict["priority"] = priority
        if dedicated_worker is not UNSET:
            field_dict["dedicated_worker"] = dedicated_worker

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_flow_json_body_schema import UpdateFlowJsonBodySchema
        from ..models.update_flow_json_body_value import UpdateFlowJsonBodyValue

        d = src_dict.copy()
        summary = d.pop("summary")

        value = UpdateFlowJsonBodyValue.from_dict(d.pop("value"))

        path = d.pop("path")

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, UpdateFlowJsonBodySchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = UpdateFlowJsonBodySchema.from_dict(_schema)

        tag = d.pop("tag", UNSET)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        priority = d.pop("priority", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        update_flow_json_body = cls(
            summary=summary,
            value=value,
            path=path,
            description=description,
            schema=schema,
            tag=tag,
            ws_error_handler_muted=ws_error_handler_muted,
            priority=priority,
            dedicated_worker=dedicated_worker,
        )

        update_flow_json_body.additional_properties = d
        return update_flow_json_body

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
