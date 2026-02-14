from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable


# ---------------------------------------------------------------------------
# Types shared by nodes and walkers
# ---------------------------------------------------------------------------


class ConflictPolicy(Enum):
    KEEP = auto()
    REPLACE = auto()


@dataclass(frozen=True)
class Behavior:
    sort_key: Callable[[Any], str] | None
    conflict_policy: ConflictPolicy = ConflictPolicy.KEEP


class Node(Protocol):
    @property
    def opaque(self) -> bool: ...
    def __call__(self, prop: str) -> tuple[Node, Behavior]: ...


_NO_BHV = Behavior(sort_key=None)


# ---------------------------------------------------------------------------
# Concrete nodes
# ---------------------------------------------------------------------------


class DataNode:
    opaque = True

    def __init__(self, name: str = "data") -> None:
        self._name = name

    def __call__(self, prop: str) -> tuple[Node, Behavior]:
        return (self, _NO_BHV)

    def __repr__(self) -> str:
        return self._name


class MapNode:
    opaque = False

    def __init__(self, name: str) -> None:
        self._name = name
        self._child: Node | None = None
        self._behavior: Behavior = _NO_BHV

    def configure(
        self,
        child: Node,
        behavior: Behavior = _NO_BHV,
    ) -> None:
        self._child = child
        self._behavior = behavior

    def __call__(self, prop: str) -> tuple[Node, Behavior]:
        assert self._child is not None, f"{self._name} not configured"
        return (self._child, self._behavior)

    def __repr__(self) -> str:
        return self._name


class ObjectNode:
    opaque = False

    def __init__(self, name: str) -> None:
        self._name = name
        self._table: dict[str, tuple[Node, Behavior]] = {}

    def configure(
        self,
        table: dict[str, tuple[Node, Behavior]],
    ) -> None:
        self._table = table

    def __call__(self, prop: str) -> tuple[Node, Behavior]:
        return self._table.get(prop, (data, _NO_BHV))

    def __repr__(self) -> str:
        return self._name


class SchemaNode:
    """JSON Schema keyword dispatch.

    - x-* extensions -> data
    - Known keywords -> looked up in table
    - Unknown keywords -> (self, _NO_BHV) (recursive, assume sub-schema)
    """

    opaque = False

    def __init__(self, name: str = "schema") -> None:
        self._name = name
        self._keywords: dict[str, tuple[Node, Behavior]] = {}

    def configure(
        self,
        keywords: dict[str, tuple[Node, Behavior]],
    ) -> None:
        self._keywords = keywords

    def __call__(self, prop: str) -> tuple[Node, Behavior]:
        if prop.startswith("x-"):
            return (data, _NO_BHV)
        return self._keywords.get(prop, (self, _NO_BHV))

    def __repr__(self) -> str:
        return self._name


# Module-level singleton: the universal trap state
data = DataNode()
