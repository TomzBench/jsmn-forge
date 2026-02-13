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


def normalize(
    obj: Any,
    context: tuple[Transition, Behavior],
    loc: Location = (),
) -> Any:
    (transition, behavior) = context
    if isinstance(obj, dict):
        return {
            key: normalize(val, transition(key), (*loc, key))
            for (key, val) in obj.items()
        }
    if isinstance(obj, list):
        sort_key = behavior.sort_key
        items = [
            normalize(item, context, (*loc, str(i)))
            for i, item in enumerate(obj)
        ]
        return sorted(items, key=sort_key) if sort_key else items
    return obj


def merge(
    dst: Any,
    src: Any,
    context: tuple[Transition, Behavior],
    loc: Location = (),
) -> MergeResult:
    conflicts: list[MergeConflict] = []
    (transition, behavior) = context
    if isinstance(dst, dict) and isinstance(src, dict):
        result = dict(dst)
        for k, v in src.items():
            child = transition(k)
            child_loc = (*loc, k)
            if k not in result:
                result[k] = deepcopy(v)
            else:
                (x, c) = merge(result[k], v, child, child_loc)
                conflicts.extend(c)
                result[k] = x
        return MergeResult(result, conflicts)

    if isinstance(dst, list) and isinstance(src, list):
        sort_key = behavior.sort_key
        if sort_key:
            # NOTE sort_key is behaving like an "identity"
            #      convert list into dict for set like symantics
            seen = {sort_key(x): x for x in dst}
            for item in src:
                k = sort_key(item)
                if k not in seen:
                    seen[k] = deepcopy(item)
                elif seen[k] != item:
                    conflicts.append(MergeConflict(loc, seen[k], item))
                    if behavior.conflict_policy == ConflictPolicy.REPLACE:
                        seen[k] = deepcopy(item)
            return MergeResult(
                sorted(seen.values(), key=sort_key),
                conflicts,
            )
        else:
            lresult = list(dst)
            n = min(len(dst), len(src))
            for i in range(n):
                if lresult[i] != src[i]:
                    (x, c) = merge(lresult[i], src[i], context, (*loc, str(i)))
                    conflicts.extend(c)
                    lresult[i] = x
            lresult += [deepcopy(x) for x in src[n:]]
            return MergeResult(lresult, conflicts)

    if dst != src:
        v = dst if behavior.conflict_policy == ConflictPolicy.KEEP else src
        return MergeResult(v, [MergeConflict(loc, dst, src)])
    else:
        return MergeResult(dst, [])
