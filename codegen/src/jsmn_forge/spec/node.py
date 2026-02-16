from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable


class ConflictPolicy(Enum):
    KEEP = auto()
    REPLACE = auto()


@dataclass(frozen=True)
class Behavior:
    sort_key: Callable[[Any], str] | None
    conflict_policy: ConflictPolicy = ConflictPolicy.KEEP


class Node(Protocol):
    @property
    def kind(self) -> str: ...
    @property
    def opaque(self) -> bool: ...
    def child(self, prop: str) -> tuple[Node, Behavior]: ...


_NO_BHV = Behavior(sort_key=None)


class DataNode:
    opaque = True

    def __init__(self, kind: str = "data") -> None:
        self._kind = kind

    @property
    def kind(self) -> str:
        return self._kind

    def child(self, prop: str) -> tuple[Node, Behavior]:
        return (self, _NO_BHV)

    def __repr__(self) -> str:
        return str(self._kind)


class MapNode[E: str]:
    opaque = False

    def __init__(self, kind: E) -> None:
        self._kind = kind
        self._child: Node | None = None
        self._behavior: Behavior = _NO_BHV

    @property
    def kind(self) -> E:
        return self._kind

    def configure(
        self,
        child: Node,
        behavior: Behavior = _NO_BHV,
    ) -> None:
        self._child = child
        self._behavior = behavior

    def child(self, prop: str) -> tuple[Node, Behavior]:
        assert self._child is not None, f"{self._kind} not configured"
        return (self._child, self._behavior)

    def __repr__(self) -> str:
        return str(self._kind)


class ObjectNode[E: str]:
    opaque = False

    def __init__(self, kind: E) -> None:
        self._kind = kind
        self._table: dict[str, tuple[Node, Behavior]] = {}

    @property
    def kind(self) -> E:
        return self._kind

    def configure(
        self,
        table: dict[str, tuple[Node, Behavior]],
    ) -> None:
        self._table = table

    def child(self, prop: str) -> tuple[Node, Behavior]:
        return self._table.get(prop, (data, _NO_BHV))

    def __repr__(self) -> str:
        return str(self._kind)


# Module-level singleton: the universal trap state
data = DataNode()
