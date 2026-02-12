from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, NamedTuple, Protocol

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


class Lookup[E: Enum](Protocol):
    @staticmethod
    def child(kind: E, key: str) -> E: ...

    @staticmethod
    def behavior(kind: E) -> Behavior: ...


def normalizer[E: Enum](lookup: Lookup[E]) -> Callable[[Any, E], Any]:
    def normalize(obj: Any, node: E, loc: Location = ()) -> Any:
        if isinstance(obj, dict):
            return {
                key: normalize(val, lookup.child(node, key), (*loc, key))
                for (key, val) in obj.items()
            }
        if isinstance(obj, list):
            sort_key = lookup.behavior(node).sort_key
            items = [
                normalize(item, node, (*loc, str(i)))
                for i, item in enumerate(obj)
            ]
            return sorted(items, key=sort_key) if sort_key else items
        return obj

    return normalize


def merger[E: Enum](
    lookup: Lookup[E],
) -> Callable[[Any, Any, E, Location], MergeResult]:
    def merge(dst: Any, src: Any, node: E, loc: Location = ()) -> MergeResult:
        conflicts: list[MergeConflict] = []
        behavior = lookup.behavior(node)
        if isinstance(dst, dict) and isinstance(src, dict):
            result = dict(dst)
            for k, v in src.items():
                child = lookup.child(node, k)
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
                        (x, c) = merge(lresult[i], src[i], node, (*loc, str(i)))
                        conflicts.extend(c)
                        lresult[i] = x
                lresult += [deepcopy(x) for x in src[n:]]
                return MergeResult(lresult, conflicts)

        if dst != src:
            v = dst if behavior.conflict_policy == ConflictPolicy.KEEP else src
            return MergeResult(v, [MergeConflict(loc, dst, src)])
        else:
            return MergeResult(dst, [])

    return merge
