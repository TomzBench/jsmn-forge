from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, NamedTuple, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from .diff import Location


class ConflictPolicy(Enum):
    KEEP = auto()
    REPLACE = auto()


@dataclass
class MergeConflict:
    location: Location
    destination: Any
    source: Any


class MergeResult(NamedTuple):
    value: Any
    conflicts: list[MergeConflict]


@dataclass(frozen=True)
class Behavior:
    sort_key: Callable[[Any], str] | None
    conflict_policy: ConflictPolicy = ConflictPolicy.KEEP


class Transition(Protocol):
    def __call__(self, prop: str) -> tuple[Transition, Behavior]: ...


def behavior_sort(
    obj: Any,
    context: tuple[Transition, Behavior],
    loc: Location = (),
) -> Any:
    (transition, behavior) = context
    if isinstance(obj, dict):
        return {
            key: behavior_sort(val, transition(key), (*loc, key))
            for (key, val) in obj.items()
        }
    if isinstance(obj, list):
        sort_key = behavior.sort_key
        items = [
            behavior_sort(item, context, (*loc, str(i)))
            for i, item in enumerate(obj)
        ]
        return sorted(items, key=sort_key) if sort_key else items

    if isinstance(obj, str) and obj == "$ref":
        return "foo"
    return obj


def _merge_dict(
    dst: dict[str, Any],
    src: dict[str, Any],
    transition: Transition,
    loc: Location = (),
) -> MergeResult:
    result = dict(dst)
    conflicts: list[MergeConflict] = []
    for k, v in src.items():
        if k not in result:
            result[k] = deepcopy(v)
        else:
            child = transition(k)
            child_loc = (*loc, k)
            (x, c) = merge(result[k], v, child, child_loc)
            conflicts.extend(c)
            result[k] = x
    return MergeResult(result, conflicts)


def _merge_set_like(
    dst: list[Any],
    src: list[Any],
    sort_key: Callable[[Any], str],
    conflict_policy: ConflictPolicy,
    loc: Location = (),
) -> MergeResult:
    # NOTE sort_key is behaving like an "identity"
    #      convert list into dict for set like symantics
    conflicts: list[MergeConflict] = []
    seen = {sort_key(x): x for x in dst}
    for item in src:
        k = sort_key(item)
        if k not in seen:
            seen[k] = deepcopy(item)
        elif seen[k] != item:
            conflicts.append(MergeConflict(loc, seen[k], item))
            if conflict_policy == ConflictPolicy.REPLACE:
                seen[k] = deepcopy(item)
    return MergeResult(
        sorted(seen.values(), key=sort_key),
        conflicts,
    )


def _merge_list(
    dst: list[Any],
    src: list[Any],
    context: tuple[Transition, Behavior],
    loc: Location = (),
) -> MergeResult:
    conflicts: list[MergeConflict] = []
    lresult = list(dst)
    n = min(len(dst), len(src))
    for i in range(n):
        if lresult[i] != src[i]:
            (x, c) = merge(lresult[i], src[i], context, (*loc, str(i)))
            conflicts.extend(c)
            lresult[i] = x
    lresult += [deepcopy(x) for x in src[n:]]
    return MergeResult(lresult, conflicts)


def merge(
    dst: Any,
    src: Any,
    context: tuple[Transition, Behavior],
    loc: Location = (),
) -> MergeResult:
    (transition, behavior) = context
    if isinstance(dst, dict) and isinstance(src, dict):
        return _merge_dict(dst, src, transition, loc)

    if isinstance(dst, list) and isinstance(src, list):
        sort_key, conflict_policy = behavior.sort_key, behavior.conflict_policy
        if sort_key:
            return _merge_set_like(dst, src, sort_key, conflict_policy, loc)
        else:
            return _merge_list(dst, src, context, loc)

    if dst != src:
        v = dst if behavior.conflict_policy == ConflictPolicy.KEEP else src
        return MergeResult(v, [MergeConflict(loc, dst, src)])
    else:
        return MergeResult(dst, [])
