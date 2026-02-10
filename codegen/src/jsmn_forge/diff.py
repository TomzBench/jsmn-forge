from dataclasses import dataclass
from typing import Any


@dataclass
class Missing:
    value: Any


@dataclass
class Extra:
    value: Any


@dataclass
class MissMatch:
    self: Any
    other: Any


type Diff = Missing | Extra | MissMatch
type Location = tuple[str, ...]


def diff(a: Any, b: Any, loc: Location = ()) -> dict[Location, Diff]:
    if isinstance(a, dict) and isinstance(b, dict):
        ret = {}
        for k in set(a) | set(b):
            key: Location = (*loc, k)
            if k not in b:
                ret[key] = Missing(a[k])
            elif k not in a:
                ret[key] = Extra(b[k])
            else:
                nested = diff(a[k], b[k], key)
                if nested:
                    ret |= {k: v for (k, v) in nested.items()}
        return ret
    elif isinstance(a, list) and isinstance(b, list):
        ret = {}
        for i in range(max(len(a), len(b))):
            key = (*loc, str(i))
            if i >= len(a):
                ret[key] = Extra(b[i])
            elif i >= len(b):
                ret[key] = Missing(a[i])
            else:
                nested = diff(a[i], b[i], key)
                if nested:
                    ret |= {k: v for (k, v) in nested.items()}

        return ret
    elif a != b:
        return {loc: MissMatch(a, b)}
    else:
        return {}
