from __future__ import annotations

from enum import StrEnum

from .behavior import canonical
from .node import _NO_BHV, Behavior, MapNode, Node, data


class SchemaKind(StrEnum):
    SCHEMA         = "schema"
    MAP_SCHEMA     = "map_schema"
    MAP_STRING_SET = "map_string_set"


# ---------------------------------------------------------------------------
# SchemaNode
# ---------------------------------------------------------------------------


class SchemaNode:
    """JSON Schema keyword dispatch.

    - x-* extensions -> data
    - Known keywords -> looked up in table
    - Unknown keywords -> (self, _NO_BHV) (recursive, assume sub-schema)
    """

    opaque = False

    def __init__(self, kind: str = "schema") -> None:
        self._kind = kind
        self._keywords: dict[str, tuple[Node, Behavior]] = {}

    @property
    def kind(self) -> str:
        return self._kind

    def configure(
        self,
        keywords: dict[str, tuple[Node, Behavior]],
    ) -> None:
        self._keywords = keywords

    def child(self, prop: str) -> tuple[Node, Behavior]:
        if prop.startswith("x-"):
            return (data, _NO_BHV)
        return self._keywords.get(prop, (self, _NO_BHV))

    def __repr__(self) -> str:
        return str(self._kind)


# ---------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------

map_schema     = MapNode(SchemaKind.MAP_SCHEMA)
map_string_set = MapNode(SchemaKind.MAP_STRING_SET)
schema         = SchemaNode(SchemaKind.SCHEMA)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

map_schema.configure(child=schema)
map_string_set.configure(child=data, behavior=Behavior(sort_key=str))

# fmt: off
schema.configure(keywords={
    # Sub-schema maps (user-defined keys → schemas)
    "properties":               (map_schema, _NO_BHV),
    "$defs":                    (map_schema, _NO_BHV),
    "patternProperties":        (map_schema, _NO_BHV),
    "dependentSchemas":         (map_schema, _NO_BHV),
    # String set map
    "dependentRequired":        (map_string_set, _NO_BHV),
    # Data-carrying keywords
    "default":                  (data, _NO_BHV),
    "example":                  (data, _NO_BHV),
    "const":                    (data, _NO_BHV),
    "examples":                 (data, Behavior(sort_key=canonical)),
    # OpenAPI / AsyncAPI extensions (objects, not schemas)
    "discriminator":            (data, _NO_BHV),
    "xml":                      (data, _NO_BHV),
    "externalDocs":             (data, _NO_BHV),
    # Set-like arrays (sorted)
    "required":                 (schema, Behavior(sort_key=str)),
    "enum":                     (schema, Behavior(sort_key=canonical)),
    "type":                     (schema, Behavior(sort_key=str)),
    "anyOf":                    (schema, Behavior(sort_key=canonical)),
    "oneOf":                    (schema, Behavior(sort_key=canonical)),
    "allOf":                    (schema, Behavior(sort_key=canonical)),
})
# fmt: on
