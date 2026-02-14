from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Any, NamedTuple

from ruamel.yaml import YAML

from .node import _NO_BHV, MapNode, ObjectNode, data
from .schema import map_schema, schema
from .sort import canonical, identity_key
from .walk import Behavior, behavior_sort
from .walk import MergeConflict as _MergeConflict
from .walk import merge as _merge

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from .diff import Location

_param_key = identity_key("in", "name")


# ---------------------------------------------------------------------------
# Phase 1: Create all node instances
# ---------------------------------------------------------------------------

obj_root = ObjectNode("obj_root")
obj_info = ObjectNode("obj_info")
obj_components = ObjectNode("obj_components")
obj_path_item = ObjectNode("obj_path_item")
obj_operation = ObjectNode("obj_operation")
obj_parameter = ObjectNode("obj_parameter")
obj_request_body = ObjectNode("obj_request_body")
obj_response = ObjectNode("obj_response")
obj_media_type = ObjectNode("obj_media_type")
obj_encoding = ObjectNode("obj_encoding")
obj_server = ObjectNode("obj_server")
obj_server_var = ObjectNode("obj_server_var")
obj_link = ObjectNode("obj_link")

map_path_item = MapNode("map_path_item")
map_response = MapNode("map_response")
map_content = MapNode("map_content")
map_header = MapNode("map_header")
map_encoding = MapNode("map_encoding")
map_parameter = MapNode("map_parameter")
map_request_body = MapNode("map_request_body")
map_link = MapNode("map_link")
map_callback = MapNode("map_callback")
map_server_var = MapNode("map_server_var")
map_scope = MapNode("map_scope")


# ---------------------------------------------------------------------------
# Phase 2: Configure (all instances exist, mutual refs work)
# ---------------------------------------------------------------------------

# fmt: off
obj_root.configure(table={
    "paths":                        (map_path_item, _NO_BHV),
    "webhooks":                     (map_path_item, _NO_BHV),
    "components":                   (obj_components, _NO_BHV),
    "servers":                      (obj_server, _NO_BHV),
    "security":                     (map_scope, Behavior(sort_key=canonical)),
})

obj_info.configure(table={})

obj_components.configure(table={
    "schemas":                      (map_schema, _NO_BHV),
    "parameters":                   (map_parameter, _NO_BHV),
    "headers":                      (map_header, _NO_BHV),
    "requestBodies":                (map_request_body, _NO_BHV),
    "responses":                    (map_response, _NO_BHV),
    "pathItems":                    (map_path_item, _NO_BHV),
    "callbacks":                    (map_callback, _NO_BHV),
    "links":                        (map_link, _NO_BHV),
})

obj_path_item.configure(table={
    "get":                          (obj_operation, _NO_BHV),
    "put":                          (obj_operation, _NO_BHV),
    "post":                         (obj_operation, _NO_BHV),
    "delete":                       (obj_operation, _NO_BHV),
    "options":                      (obj_operation, _NO_BHV),
    "head":                         (obj_operation, _NO_BHV),
    "patch":                        (obj_operation, _NO_BHV),
    "trace":                        (obj_operation, _NO_BHV),
    "parameters":                   (obj_parameter, Behavior(sort_key=_param_key)),
    "servers":                      (obj_server, _NO_BHV),
})

obj_operation.configure(table={
    "requestBody":                  (obj_request_body, _NO_BHV),
    "responses":                    (map_response, _NO_BHV),
    "callbacks":                    (map_callback, _NO_BHV),
    "parameters":                   (obj_parameter, Behavior(sort_key=_param_key)),
    "servers":                      (obj_server, _NO_BHV),
    "security":                     (map_scope, Behavior(sort_key=canonical)),
    "tags":                         (data, Behavior(sort_key=str)),
})

obj_parameter.configure(table={
    "schema":                       (schema, _NO_BHV),
    "content":                      (map_content, _NO_BHV),
})

obj_request_body.configure(table={
    "content":                      (map_content, _NO_BHV),
})

obj_response.configure(table={
    "content":                      (map_content, _NO_BHV),
    "headers":                      (map_header, _NO_BHV),
    "links":                        (map_link, _NO_BHV),
})

obj_media_type.configure(table={
    "schema":                       (schema, _NO_BHV),
    "encoding":                     (map_encoding, _NO_BHV),
})

obj_encoding.configure(table={
    "headers":                      (map_header, _NO_BHV),
})

obj_server.configure(table={
    "variables":                    (map_server_var, _NO_BHV),
})

obj_server_var.configure(table={
    "enum":                         (data, Behavior(sort_key=str)),
})

obj_link.configure(table={
    "server":                       (obj_server, _NO_BHV),
})

map_path_item.configure(child=obj_path_item)
map_response.configure(child=obj_response)
map_content.configure(child=obj_media_type)
map_header.configure(child=obj_parameter)
map_encoding.configure(child=obj_encoding)
map_parameter.configure(child=obj_parameter)
map_request_body.configure(child=obj_request_body)
map_link.configure(child=obj_link)
map_callback.configure(child=map_path_item)
map_server_var.configure(child=obj_server_var)
map_scope.configure(child=data, behavior=Behavior(sort_key=str))
# fmt: on


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------


@dataclass
class MergeConflict:
    file: Path
    location: Location
    destination: Any
    source: Any


@dataclass
class FileNotFound:
    path: Path


class Specification(NamedTuple):
    file: Path
    data: Any


type MergeError = FileNotFound
type NormalizeResult = tuple[list[Specification], list[FileNotFound]]

yaml = YAML(typ="safe")


@dataclass
class MergeResult:
    value: Any
    conflicts: list[MergeConflict]
    errors: list[MergeError]


def upgrade_conflict(file: Path) -> Callable[[_MergeConflict], MergeConflict]:
    def upgrader(conflict: _MergeConflict) -> MergeConflict:
        return MergeConflict(
            file=file,
            location=conflict.location,
            destination=conflict.destination,
            source=conflict.source,
        )

    return upgrader


def merge(*args: Path) -> MergeResult:
    root = (obj_root, _NO_BHV)

    def sort_step(acc: NormalizeResult, next: Path) -> NormalizeResult:
        try:
            behavior_sorted = behavior_sort(yaml.load(next), root)
            spec = Specification(next, behavior_sorted)
            acc[0].append(spec)
        except FileNotFoundError:
            acc[1].append(FileNotFound(next))
        return acc

    def merge_step(acc: MergeResult, spec: Specification) -> MergeResult:
        (file, src) = spec
        (r, c) = _merge(acc.value, src, root)
        conflicts = list(map(upgrade_conflict(file), c))
        # TODO evaluate conflicts. Upgrade some to errors
        #      (ie: info.version missmatch)
        return MergeResult(r, acc.conflicts + conflicts, [])

    # Behavior sort all the input files
    init: NormalizeResult = ([], [])
    (behavior_sorted, errors) = reduce(sort_step, args, init)

    rest = iter(behavior_sorted)
    try:
        # Pop the first specification off the list for which merge will appy
        (_, first) = next(rest)
        # Merge remaining specifications
        result = reduce(merge_step, rest, MergeResult(first, [], errors))
        return result
    except StopIteration as _e:
        return MergeResult(None, [], errors)
