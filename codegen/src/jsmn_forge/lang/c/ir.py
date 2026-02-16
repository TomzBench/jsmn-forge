"""C IR — output of the flatten pass, input to C codegen.

Four types model the entire C codegen input:

  CType   — hashable type identifier: (name, dims)
  Dim     — array dimension with min/max bounds
  Field   — struct member: name + CType (or tuple[CType,...] for tagged union)
  CStruct — named struct definition with fields

Everything else — VLA wrappers, optional wrappers, union wrappers, mangled
names, token counts, dependency order — is derived by codegen from these types.

A CType with dims where min != max implies a VLA wrapper struct.
A Field with required=False implies an optional wrapper struct.
A Field with tuple[CType, ...] implies a tagged union wrapper.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from jsmn_forge.node import Location


class Dim(NamedTuple):
    """Array dimension — one level in a (possibly multi-dimensional) array.

    Outer-to-inner order: dims[0] is the outermost array.
    min == max → fixed dimension (e.g., char name[32])
    min != max → variable length array (capacity = max)
    """

    min: int
    max: int


class CType(NamedTuple):
    """Hashable C type identifier.

    name: resolved C type name — "bool", "uint32_t", "char", "foo"
    dims:  array shape, outer-to-inner

    Examples:
        CType("uint32_t")                      → uint32_t (scalar)
        CType("char", (Dim(32, 32),))          → char[32] (string)
        CType("uint8_t", (Dim(64, 64),))       → uint8_t[64] (byte array)
        CType("uint32_t", (Dim(0, 3),))        → vla wrapper (VLA, capacity 3)
        CType("foo")                            → struct foo (ref)
        CType("foo", (Dim(0, 10),))            → vla wrapper of struct foo
    """

    name: str
    dims: tuple[Dim, ...] = ()


@dataclass
class Field:
    """Struct member.

    When ctype is a tuple of CTypes, the field is a tagged union of those
    variant types.  Codegen derives the union wrapper struct and its mangled
    name from the variant list.
    """

    name: str
    ctype: CType | tuple[CType, ...]
    required: bool = True


@dataclass
class CStruct:
    """Named C struct definition — the primary codegen unit."""

    ctype: CType
    loc: Location
    fields: list[Field]
