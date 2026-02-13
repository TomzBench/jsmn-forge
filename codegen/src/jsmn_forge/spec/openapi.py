from __future__ import annotations

from jsmn_forge.spec.schema import data, map_schema, schema
from jsmn_forge.spec.sort import SortKey, canonical, identity_key
from jsmn_forge.spec.walk import Behavior, Transition

_NO_BHV = Behavior(sort_key=None)
_param_key = identity_key("in", "name")


# ---------------------------------------------------------------------------
# Dispatchers
# ---------------------------------------------------------------------------


def _resolve_obj(key: Transition, prop: str) -> tuple[Transition, Behavior]:
    table = _OBJ[key]
    child = table.get(prop, data)
    sort = _SORT.get(key, {}).get(prop)
    bhv = Behavior(sort_key=sort) if sort else _NO_BHV
    return (child, bhv)


def _resolve_map(key: Transition, prop: str) -> tuple[Transition, Behavior]:
    child = _MAP[key]
    sort = _DEFAULT_SORT.get(key)
    bhv = Behavior(sort_key=sort) if sort else _NO_BHV
    return (child, bhv)


# ---------------------------------------------------------------------------
# Object transitions
# ---------------------------------------------------------------------------


def obj_root(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_root, prop)


def obj_info(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_info, prop)


def obj_components(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_components, prop)


def obj_path_item(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_path_item, prop)


def obj_operation(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_operation, prop)


def obj_parameter(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_parameter, prop)


def obj_request_body(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_request_body, prop)


def obj_response(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_response, prop)


def obj_media_type(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_media_type, prop)


def obj_encoding(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_encoding, prop)


def obj_server(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_server, prop)


def obj_server_var(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_server_var, prop)


def obj_link(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_obj(obj_link, prop)


# ---------------------------------------------------------------------------
# Map transitions
# ---------------------------------------------------------------------------


def map_path_item(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_path_item, prop)


def map_response(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_response, prop)


def map_content(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_content, prop)


def map_header(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_header, prop)


def map_encoding(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_encoding, prop)


def map_parameter(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_parameter, prop)


def map_request_body(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_request_body, prop)


def map_link(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_link, prop)


def map_callback(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_callback, prop)


def map_server_var(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_server_var, prop)


def map_scope(prop: str) -> tuple[Transition, Behavior]:
    return _resolve_map(map_scope, prop)


# ---------------------------------------------------------------------------
# Object child tables
# ---------------------------------------------------------------------------

# fmt: off
_ROOT: dict[str, Transition] = {
    "paths":                        map_path_item,
    "webhooks":                     map_path_item,
    "components":                   obj_components,
    "servers":                      obj_server,
    "security":                     map_scope,
}

_COMPONENTS: dict[str, Transition] = {
    "schemas":                      map_schema,
    "parameters":                   map_parameter,
    "headers":                      map_header,
    "requestBodies":                map_request_body,
    "responses":                    map_response,
    "pathItems":                    map_path_item,
    "callbacks":                    map_callback,
    "links":                        map_link,
}

_PATH_ITEM: dict[str, Transition] = {
    "get":                          obj_operation,
    "put":                          obj_operation,
    "post":                         obj_operation,
    "delete":                       obj_operation,
    "options":                      obj_operation,
    "head":                         obj_operation,
    "patch":                        obj_operation,
    "trace":                        obj_operation,
    "parameters":                   obj_parameter,
    "servers":                      obj_server,
}

_OPERATION: dict[str, Transition] = {
    "requestBody":                  obj_request_body,
    "responses":                    map_response,
    "callbacks":                    map_callback,
    "parameters":                   obj_parameter,
    "servers":                      obj_server,
    "security":                     map_scope,
}

_PARAMETER: dict[str, Transition] = {
    "schema":                       schema,
    "content":                      map_content,
}

_REQUEST_BODY: dict[str, Transition] = {
    "content":                      map_content,
}

_RESPONSE: dict[str, Transition] = {
    "content":                      map_content,
    "headers":                      map_header,
    "links":                        map_link,
}

_MEDIA_TYPE: dict[str, Transition] = {
    "schema":                       schema,
    "encoding":                     map_encoding,
}

_ENCODING: dict[str, Transition] = {
    "headers":                      map_header,
}

_SERVER: dict[str, Transition] = {
    "variables":                    map_server_var,
}

_LINK: dict[str, Transition] = {
    "server":                       obj_server,
}
# fmt: on


# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

# fmt: off
_OBJ: dict[Transition, dict[str, Transition]] = {
    obj_root:                       _ROOT,
    obj_info:                       {},
    obj_components:                 _COMPONENTS,
    obj_path_item:                  _PATH_ITEM,
    obj_operation:                  _OPERATION,
    obj_parameter:                  _PARAMETER,
    obj_request_body:               _REQUEST_BODY,
    obj_response:                   _RESPONSE,
    obj_media_type:                 _MEDIA_TYPE,
    obj_encoding:                   _ENCODING,
    obj_server:                     _SERVER,
    obj_server_var:                 {},
    obj_link:                       _LINK,
}

_MAP: dict[Transition, Transition] = {
    map_path_item:                  obj_path_item,
    map_response:                   obj_response,
    map_content:                    obj_media_type,
    map_header:                     obj_parameter,
    map_encoding:                   obj_encoding,
    map_parameter:                  obj_parameter,
    map_request_body:               obj_request_body,
    map_link:                       obj_link,
    map_callback:                   map_path_item,
    map_server_var:                 obj_server_var,
    map_scope:                      data,
}

_SORT: dict[Transition, dict[str, SortKey]] = {
    obj_root: {
        "security":                 canonical,
    },
    obj_operation: {
        "security":                 canonical,
        "parameters":               _param_key,
        "tags":                     str,
    },
    obj_path_item: {
        "parameters":               _param_key,
    },
    obj_server_var: {
        "enum":                     str,
    },
}

_DEFAULT_SORT: dict[Transition, SortKey] = {
    map_scope:                      str,
}
# fmt: on
