from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


@dataclass(frozen=True)
class Behavior(Protocol):
    sort_key: Callable[[Any], str] | None


class Lookup[E: Enum](Protocol):
    @staticmethod
    def child(kind: E, key: str) -> E: ...

    @staticmethod
    def behavior(kind: E) -> Behavior: ...


def normalizer[E: Enum](lookup: Lookup[E]) -> Callable[[Any, E], Any]:
    def normalize(obj: Any, node: E) -> Any:
        if isinstance(obj, dict):
            return {
                key: normalize(val, lookup.child(node, key))
                for (key, val) in obj.items()
            }
        if isinstance(obj, list):
            sort_key = lookup.behavior(node).sort_key
            items = [normalize(v, node) for v in obj]
            return sorted(items, key=sort_key) if sort_key else items
        return obj

    return normalize


def merger[E: Enum](lookup: Lookup[E]) -> Callable[[Any, Any, E], Any]:
    def merge(dst: Any, src: Any, node: E) -> Any:
        if isinstance(dst, dict) and isinstance(src, dict):
            result = dict(dst)
            for k, v in src.items():
                if k not in result:
                    result[k] = deepcopy(v)
                else:
                    result[k] = merge(result[k], v, lookup.child(node, k))
            return result
        if isinstance(dst, list) and isinstance(src, list):
            result = list(dst)
            sort_key = lookup.behavior(node).sort_key
            if sort_key:
                seen = {sort_key(x): x for x in dst}
                for item in src:
                    k = sort_key(item)
                    if k not in seen:
                        result.append(deepcopy(item))
                    elif seen[k] != item:
                        # TODO conflict or not
                        ...
                return sorted(result, key=sort_key)
            else:
                n = min(len(dst), len(src))
                return [
                    merge(result[i], src[i], node)
                    if result[i] != src[i]
                    else result[i]
                    for i in range(n)
                ] + [deepcopy(x) for x in src[n:]]

        if dst != src:
            # TODO a collector?
            raise NotImplementedError

    return merge
