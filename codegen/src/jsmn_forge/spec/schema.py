from __future__ import annotations

from jsmn_forge.spec.sort import SortKey, canonical
from jsmn_forge.spec.walk import Behavior, Transition

_NO_BHV = Behavior(sort_key=None)


# ---------------------------------------------------------------------------
# Sort keys for schema keywords
# ---------------------------------------------------------------------------

# fmt: off
_SORT: dict[str, SortKey] = {
    "required":                     str,
    "enum":                         canonical,
    "type":                         str,
    "anyOf":                        canonical,
    "oneOf":                        canonical,
    "allOf":                        canonical,
    "examples":                     canonical,
}
# fmt: on


# ---------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------


def data(prop: str) -> tuple[Transition, Behavior]:
    """Opaque data — trap state. All children are more data."""
    return (data, _NO_BHV)


def map_schema(prop: str) -> tuple[Transition, Behavior]:
    """Map where all values are JSON Schemas ({name: Schema})."""
    return (schema, _NO_BHV)


def map_string_set(prop: str) -> tuple[Transition, Behavior]:
    """Map where all values are sorted string arrays ({name: string[]})."""
    return (data, Behavior(sort_key=str))


# fmt: off
_KEYWORDS: dict[str, Transition] = {
    # Sub-schema maps (user-defined keys → schemas)
    "properties":               map_schema,
    "$defs":                    map_schema,
    "patternProperties":        map_schema,
    "dependentSchemas":         map_schema,
    # String set map
    "dependentRequired":        map_string_set,
    # Data-carrying keywords
    "default":                  data,
    "example":                  data,
    "const":                    data,
    "examples":                 data,
    # OpenAPI / AsyncAPI extensions (objects, not schemas)
    "discriminator":            data,
    "xml":                      data,
    "externalDocs":             data,
}
# fmt: on


def schema(prop: str) -> tuple[Transition, Behavior]:
    """JSON Schema keyword dispatch.

    - Unrecognized keywords → schema (sub-schemas)
    - x-* extensions → data
    - Known keywords (schema maps, string sets, data) → resolved here
    """
    if prop.startswith("x-"):
        return (data, _NO_BHV)
    sort = _SORT.get(prop)
    bhv = Behavior(sort_key=sort) if sort else _NO_BHV
    kw = _KEYWORDS.get(prop)
    return (kw, bhv) if kw else (schema, bhv)
