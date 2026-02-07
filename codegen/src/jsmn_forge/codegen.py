"""IR Descriptors — output of the flatten pass, input to codegen."""

from dataclasses import dataclass
from typing import Literal, NamedTuple

# Number formats (integer + number types)
NumberFormat = Literal[
    "int8",
    "int16",
    "int32",
    "int64",
    "int128",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "uint128",
    "float",
    "double",
]

# String formats
StringFormat = Literal[
    "date",
    "date-time",
    "password",
    "uuid",
    "uri",
    "email",
    "hostname",
    "ipv4",
    "ipv6",
]

# Binary formats
BinaryFormat = Literal["byte", "binary"]


class Dim(NamedTuple):
    """Array dimension — one level in a (possibly multi-dimensional) array.

    Outer-to-inner order: dims[0] is the outermost array.
    """

    min: int
    max: int


class Bound(NamedTuple):
    """Inclusive or exclusive bound for numeric range validation."""

    value: float
    exclusive: bool = False


# ---------------------------------------------------------------------------
# Field types — discriminated by `kind`. When `dims` is present, the field
# is an array (possibly multi-dimensional) of the base type.
# ---------------------------------------------------------------------------


@dataclass
class BoolType:
    kind: Literal["bool"] = "bool"
    dims: list[Dim] | None = None


@dataclass
class NullType:
    kind: Literal["null"] = "null"
    dims: list[Dim] | None = None


@dataclass
class NumberType:
    format: NumberFormat
    kind: Literal["number"] = "number"
    minimum: Bound | None = None
    maximum: Bound | None = None
    dims: list[Dim] | None = None


@dataclass
class StringType:
    max_length: int
    kind: Literal["string"] = "string"
    min_length: int | None = None
    pattern: str | None = None
    dims: list[Dim] | None = None


@dataclass
class RefType:
    """Reference to another named descriptor."""

    to: str
    kind: Literal["ref"] = "ref"
    dims: list[Dim] | None = None


FieldType = BoolType | NullType | NumberType | StringType | RefType


# ---------------------------------------------------------------------------
# Field — a single field within an ObjectDescriptor
# ---------------------------------------------------------------------------


@dataclass
class Field:
    name: str
    type: FieldType
    required: bool


# ---------------------------------------------------------------------------
# Top-level descriptors — discriminated union, switch on `kind` to narrow
# ---------------------------------------------------------------------------


@dataclass
class NullDescriptor:
    name: str
    kind: Literal["null"] = "null"


@dataclass
class BoolDescriptor:
    name: str
    kind: Literal["bool"] = "bool"


@dataclass
class NumberDescriptor:
    name: str
    format: NumberFormat
    kind: Literal["number"] = "number"
    minimum: Bound | None = None
    maximum: Bound | None = None


@dataclass
class StringDescriptor:
    name: str
    max_length: int
    kind: Literal["string"] = "string"
    min_length: int | None = None
    pattern: str | None = None


@dataclass
class ArrayDescriptor:
    name: str
    items: FieldType
    dims: list[Dim]
    kind: Literal["array"] = "array"


@dataclass
class ObjectDescriptor:
    name: str
    fields: list[Field]
    kind: Literal["object"] = "object"


Descriptor = (
    NullDescriptor
    | BoolDescriptor
    | NumberDescriptor
    | StringDescriptor
    | ArrayDescriptor
    | ObjectDescriptor
)
