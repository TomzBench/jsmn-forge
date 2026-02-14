from __future__ import annotations

from .node import MapNode, SchemaNode, _NO_BHV, data
from .sort import canonical
from .walk import Behavior

# ---------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------

map_schema = MapNode("map_schema")
map_string_set = MapNode("map_string_set")
schema = SchemaNode("schema")

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
