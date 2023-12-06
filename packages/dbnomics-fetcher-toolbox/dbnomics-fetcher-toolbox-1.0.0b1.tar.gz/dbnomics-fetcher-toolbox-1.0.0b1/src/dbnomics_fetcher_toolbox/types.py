import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final, Self, TypeAlias

from phantom.re import FullMatch

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.resource import Resource
    from dbnomics_fetcher_toolbox.resource_group import ResourceGroup

__all__ = ["ResourceFullId", "ResourceGroupId", "ResourceId"]


resource_or_group_id_regex: Final = re.compile(r"[\w-]+")


class ResourceOrGroupId(FullMatch, pattern=resource_or_group_id_regex):
    ...


ResourceGroupId: TypeAlias = ResourceOrGroupId
ResourceId: TypeAlias = ResourceOrGroupId


@dataclass(frozen=True)
class ResourceFullId:
    group_id: ResourceGroupId | None
    resource_id: ResourceId

    @classmethod
    def from_group_and_resource(cls, group: "ResourceGroup | None", resource: "Resource[Any]") -> Self:
        group_id = None if group is None else group.group_id
        return cls(group_id, resource.id)

    @classmethod
    def parse(cls, value: str) -> Self:
        group_id = None
        if "." in value:
            group_id_str, resource_id_str = value.split(".", 1)
            group_id = ResourceGroupId.parse(group_id_str)
        else:
            resource_id_str = value

        resource_id = ResourceId.parse(resource_id_str)
        return cls(group_id, resource_id)

    def __str__(self) -> str:
        if self.group_id is None:
            return str(self.resource_id)
        return f"{self.group_id}.{self.resource_id}"
