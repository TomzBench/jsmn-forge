from __future__ import annotations

from .walk import Behavior, Transition

_NO_BHV = Behavior(sort_key=None)


class DataNode:
    """Trap state. All children are opaque data."""

    def __init__(self, name: str = "data") -> None:
        self._name = name

    def __call__(self, prop: str) -> tuple[Transition, Behavior]:
        return (self, _NO_BHV)

    def __repr__(self) -> str:
        return self._name


class MapNode:
    """Uniform child transition. Every property yields the same (child, behavior)."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._child: Transition | None = None
        self._behavior: Behavior = _NO_BHV

    def configure(
        self,
        child: Transition,
        behavior: Behavior = _NO_BHV,
    ) -> None:
        self._child = child
        self._behavior = behavior

    def __call__(self, prop: str) -> tuple[Transition, Behavior]:
        assert self._child is not None, f"{self._name} not configured"
        return (self._child, self._behavior)

    def __repr__(self) -> str:
        return self._name


class ObjectNode:
    """Per-property dispatch via table lookup. Unknown properties fall through to data."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._table: dict[str, tuple[Transition, Behavior]] = {}

    def configure(
        self,
        table: dict[str, tuple[Transition, Behavior]],
    ) -> None:
        self._table = table

    def __call__(self, prop: str) -> tuple[Transition, Behavior]:
        return self._table.get(prop, (data, _NO_BHV))

    def __repr__(self) -> str:
        return self._name


class SchemaNode:
    """JSON Schema keyword dispatch.

    - x-* extensions -> data
    - Known keywords -> looked up in table
    - Unknown keywords -> (self, _NO_BHV) (recursive, assume sub-schema)
    """

    def __init__(self, name: str = "schema") -> None:
        self._name = name
        self._keywords: dict[str, tuple[Transition, Behavior]] = {}

    def configure(
        self,
        keywords: dict[str, tuple[Transition, Behavior]],
    ) -> None:
        self._keywords = keywords

    def __call__(self, prop: str) -> tuple[Transition, Behavior]:
        if prop.startswith("x-"):
            return (data, _NO_BHV)
        return self._keywords.get(prop, (self, _NO_BHV))

    def __repr__(self) -> str:
        return self._name


# Module-level singleton: the universal trap state
data = DataNode()
