from pathlib import Path
from typing import Any

from jsmn_forge.lang.c.flatten import flatten
from jsmn_forge.lang.c.ir import CType, Dim
from ruamel.yaml import YAML

yaml = YAML(typ="safe")
FIXTURES = Path(__file__).parent.parent / "fixtures" / "flatten"


def load(name: str) -> Any:
    return yaml.load(FIXTURES / name)


def test_flatten_basic_types() -> None:
    """Primitive fields (number formats, string, bool) map to correct CTypes."""
    result = flatten(load("basic_types.yaml"))
    assert result.errors == []
    assert len(result.structs) == 1
    s = result.structs[0]
    assert s.ctype == CType("sensor")
    fields = {f.name: f for f in s.fields}
    assert fields["enabled"].ctype == CType("bool")
    assert fields["enabled"].required is True
    assert fields["label"].ctype == CType("uint8_t", (Dim(32, 32),))
    assert fields["reading"].ctype == CType("double")
    assert fields["status"].ctype == CType("uint8_t")


def test_flatten_nested_object() -> None:
    """Nested object property produces a child CStruct before the parent."""
    result = flatten(load("nested_object.yaml"))
    assert result.errors == []
    assert len(result.structs) == 2
    # Child struct emitted before parent (dependency order)
    assert result.structs[0].ctype == CType("device_config")
    assert result.structs[1].ctype == CType("device")
    # Parent references child by name
    parent_fields = {f.name: f for f in result.structs[1].fields}
    assert parent_fields["config"].ctype == CType("device_config")


def test_flatten_arrays() -> None:
    """Fixed and variable-length arrays produce correct Dims."""
    result = flatten(load("arrays.yaml"))
    assert result.errors == []
    assert len(result.structs) == 1
    fields = {f.name: f for f in result.structs[0].fields}
    # Fixed array: minItems == maxItems
    assert fields["fixed_temps"].ctype == CType("int32_t", (Dim(4, 4),))
    # Variable-length array: minItems defaults to 0
    assert fields["variable_temps"].ctype == CType("int32_t", (Dim(0, 8),))
    # Array of strings: array dim + string dim
    assert fields["labels"].ctype == CType("uint8_t", (Dim(3, 3), Dim(16, 16)))
