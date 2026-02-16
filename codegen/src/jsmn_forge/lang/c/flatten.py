from dataclasses import dataclass
from functools import reduce
from typing import Any

from jsmn_forge.lang.c.ir import CStruct, CType, Dim, Field
from jsmn_forge.node import Location
from jsmn_forge.spec import OPENAPI_3_1, OpenApi31Keys
from jsmn_forge.walk import Step, walk


@dataclass
class FlattenError:
    location: Location
    message: str


@dataclass
class FlattenResult:
    structs: list[CStruct]
    errors: list[FlattenError]


_FORMAT_MAP: dict[str, str] = {
    "uint8": "uint8_t",
    "int8": "int8_t",
    "uint16": "uint16_t",
    "int16": "int16_t",
    "uint32": "uint32_t",
    "int32": "int32_t",
    "uint64": "uint64_t",
    "int64": "int64_t",
    "float": "float",
    "double": "double",
}


def _is_schema(step: Step[OpenApi31Keys]) -> bool:
    return step.kind == "schema_enter"


def _map_null(_schema: dict[str, Any]) -> CType:
    raise NotImplementedError("null type")


def _map_bool(_schema: dict[str, Any]) -> CType:
    return CType("bool")


def _map_number(schema: dict[str, Any]) -> CType:
    fmt = schema.get("format")
    name = _FORMAT_MAP.get(fmt or "")
    if name is None:
        raise ValueError(f"number without recognized format: {schema}")
    return CType(name)


def _map_string(schema: dict[str, Any]) -> CType:
    max_len = schema.get("maxLength")
    if max_len is None:
        raise ValueError(f"string without maxLength: {schema}")
    return CType("uint8_t", (Dim(max_len, max_len),))


def _resolve_array(
    parent: str,
    prop: str,
    schema: dict[str, Any],
    loc: Location,
) -> tuple[CType, list[CStruct]]:
    max_items = schema.get("maxItems")
    if max_items is None:
        raise ValueError(f"array without maxItems: {schema}")
    min_items = schema.get("minItems", 0)
    dim = Dim(min_items, max_items)
    items = schema.get("items")
    if items is None:
        raise ValueError(f"array without items: {schema}")
    inner, nested = _resolve_type(parent, prop, items, loc.push("items"))
    return CType(inner.name, (dim,) + inner.dims), nested


def _resolve_type(
    parent: str,
    prop: str,
    schema: dict[str, Any],
    loc: Location,
) -> tuple[CType, list[CStruct]]:
    if "$ref" in schema:
        raise NotImplementedError("$ref")
    if any(k in schema for k in ("allOf", "anyOf", "oneOf")):
        raise NotImplementedError("allOf/anyOf/oneOf")

    schema_type = schema.get("type")
    if schema_type == "object":
        name = f"{parent}_{prop}"
        structs = _flatten_object(name, schema, loc)
        return CType(name), structs
    if schema_type == "array":
        return _resolve_array(parent, prop, schema, loc)
    if schema_type in ("number", "integer"):
        return _map_number(schema), []
    if schema_type == "string":
        return _map_string(schema), []
    if schema_type in ("bool", "boolean"):
        return _map_bool(schema), []
    if schema_type == "null":
        return _map_null(schema), []
    raise ValueError(f"unknown schema type: {schema_type}")


def _flatten_object(
    name: str,
    schema: dict[str, Any],
    loc: Location,
) -> list[CStruct]:
    structs: list[CStruct] = []
    fields: list[Field] = []
    required = set(schema.get("required", []))
    for prop_name, prop_schema in schema.get("properties", {}).items():
        prop_loc = loc.push("properties").push(prop_name)
        ctype, nested = _resolve_type(name, prop_name, prop_schema, prop_loc)
        structs.extend(nested)
        fields.append(
            Field(
                name=prop_name,
                ctype=ctype,
                required=prop_name in required,
            )
        )
    structs.append(CStruct(ctype=CType(name), loc=loc, fields=fields))
    return structs


def _map_step(step: Step[OpenApi31Keys]) -> list[CStruct]:
    schema = step.value
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return []
    name = step.location[-1] if step.location else "unknown"
    return _flatten_object(name, schema, step.location)


def flatten(*specs: Any) -> FlattenResult:
    def step(acc: FlattenResult, s: Step[OpenApi31Keys]) -> FlattenResult:
        try:
            acc.structs.extend(_map_step(s))
        except ValueError as e:
            acc.errors.append(FlattenError(s.location, str(e)))
        return acc

    steps = filter(_is_schema, walk(*specs, draft=OPENAPI_3_1))
    return reduce(step, steps, FlattenResult([], []))
