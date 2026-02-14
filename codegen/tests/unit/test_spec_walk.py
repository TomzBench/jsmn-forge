from pathlib import Path
from typing import Any

import pytest
from jsmn_forge.spec import diff, merge
from jsmn_forge.spec.node import _NO_BHV
from jsmn_forge.spec.openapi_3_1 import obj_root
from jsmn_forge.spec.walk import normalize
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


@pytest.fixture
def walk_data() -> dict[str, Any]:
    walk = Path(__file__).parent.parent.absolute() / "fixtures" / "walk"
    # return {file.stem: yaml.load(file) for file in walk.iterdir()}
    return {file.stem: file.absolute() for file in walk.iterdir()}


def test_schema_sets(walk_data: dict[str, Any]) -> None:
    """Schema-level set arrays (required, enum, type, oneOf) normalize
    to the same result regardless of authoring order."""
    test_files = (walk_data["schema_sets_a"], walk_data["schema_sets_b"])
    result = merge(*test_files)
    assert result.conflicts == []
    widget = result.value["components"]["schemas"]["widget"]
    assert widget["required"] == ["alpha", "beta"]
    assert widget["properties"]["alpha"]["type"] == ["null", "string"]
    assert widget["properties"]["alpha"]["enum"] == ["fast", "slow"]
    # oneOf sorted by canonical:
    # {"format":..,"type":"integer"} < {"maxLength":..,"type":"string"}
    assert widget["properties"]["beta"]["oneOf"][0]["type"] == "integer"
    assert widget["properties"]["beta"]["oneOf"][1]["type"] == "string"


def test_openapi_sets(walk_data: dict[str, Any]) -> None:
    """OpenAPI-level set arrays (parameters, tags, security, scopes,
    server_var.enum) normalize equivalently regardless of order."""
    test_files = (walk_data["openapi_sets_a"], walk_data["openapi_sets_b"])
    result = merge(*test_files)
    assert result.conflicts == []
    op = result.value["paths"]["/items"]["get"]
    assert op["tags"] == ["admin", "inventory"]
    # parameters sorted by (in, name): path/id < query/limit
    assert op["parameters"][0]["name"] == "id"
    assert op["parameters"][0]["in"] == "path"
    assert op["parameters"][1]["name"] == "limit"
    assert op["parameters"][1]["in"] == "query"
    # security sorted by canonical: apiKey < oauth
    assert list(op["security"][0].keys()) == ["apiKey"]
    assert list(op["security"][1].keys()) == ["oauth"]
    # security scopes sorted by str
    assert op["security"][1]["oauth"] == ["read", "write"]
    # server_var.enum sorted by str
    server_var = result.value["servers"][0]["variables"]["env"]
    assert server_var["enum"] == ["prod", "staging"]


def test_ordered(walk_data: dict[str, Any]) -> None:
    """Ordered arrays (servers, prefixItems, root tags) must NOT be
    sorted by normalize — different authoring order stays different."""
    a = walk_data["ordered_a"]
    b = walk_data["ordered_b"]
    result = merge(a, b)
    # Ordered arrays produce positional conflicts/differences
    assert result.conflicts != []
    # Verify the diffs are real — normalize preserves order
    merged_a = merge(a)
    merged_b = merge(b)
    assert diff(merged_a.value, merged_b.value) != {}


def test_merge_union(walk_data: dict[str, Any]) -> None:
    """Disjoint + overlapping content merges cleanly: dict key union,
    required set union, new schema deep-copied."""
    test_files = (walk_data["merge_union_a"], walk_data["merge_union_b"])
    result = merge(*test_files)
    assert result.conflicts == []
    schemas = result.value["components"]["schemas"]
    # alpha: required is union of both
    assert schemas["alpha"]["required"] == ["code", "name"]
    # alpha: properties merged from both sides
    assert "name" in schemas["alpha"]["properties"]
    assert "code" in schemas["alpha"]["properties"]
    # beta: deep-copied from b
    assert "beta" in schemas
    assert schemas["beta"]["properties"]["active"]["type"] == "boolean"


def test_merge_conflict(walk_data: dict[str, Any]) -> None:
    """Conflicting scalars and parameter identity produce MergeConflict
    objects with correct locations."""
    test_files = (walk_data["merge_conflict_a"], walk_data["merge_conflict_b"])
    result = merge(*test_files)
    locs = {c.location for c in result.conflicts}
    assert ("info", "title") in locs
    assert ("info", "version") in locs
    # parameter with same (in, name) but different schema
    assert ("paths", "/items", "get", "parameters") in locs
    assert len(result.conflicts) == 3


def test_ref_rewriting(walk_data: dict[str, Any]) -> None:
    """$ref values are rewritten in schema-aware contexts but left
    untouched inside data traps (default, x-*)."""
    raw = yaml.load(walk_data["refs"])
    result = normalize(raw, (obj_root, _NO_BHV), scheme="forge")
    schemas = result["components"]["schemas"]

    # Direct $ref — local, unchanged
    assert schemas["direct"]["$ref"] == "#/components/schemas/target"

    # Properties: local unchanged, external rewritten
    props = schemas["in_properties"]["properties"]
    assert props["local"]["$ref"] == "#/components/schemas/target"
    assert (
        props["external"]["$ref"]
        == "./sdk.openapi.yaml#/components/schemas/Foo"
    )

    # allOf: scheme ref rewritten, relative ref collapsed to fragment
    allOf = schemas["in_properties"]["allOf"]
    refs = sorted(item["$ref"] for item in allOf)
    assert "#/components/schemas/Baz" in refs
    assert "./sdk.openapi.yaml#/components/schemas/Bar" in refs

    # $ref with sibling keys — ref rewritten, siblings preserved
    assert schemas["with_siblings"]["$ref"] == "#/components/schemas/target"
    assert schemas["with_siblings"]["description"] == "has sibling keys"

    # Data traps — $ref is just data, NOT rewritten
    traps = schemas["data_traps"]
    assert traps["default"]["$ref"] == "#/not_a_real_ref"
    assert traps["x-meta"]["$ref"] == "forge://sdk/common/v0#/not_a_real_ref"


def test_schema_dispatch(walk_data: dict[str, Any]) -> None:
    """Data traps (default, x-*) preserve content unchanged while
    schema-aware paths (dependentRequired, $defs, enum, examples) sort."""
    test_files = (
        walk_data["schema_dispatch_a"],
        walk_data["schema_dispatch_b"],
    )
    result = merge(*test_files)
    assert result.conflicts == []
    gadget = result.value["components"]["schemas"]["gadget"]
    name_prop = gadget["properties"]["name"]
    # default is a data trap — unsorted array preserved
    assert name_prop["default"]["required"] == ["zebra", "apple"]
    # x-meta is a data trap — unsorted array preserved
    assert name_prop["x-meta"]["tags"] == ["beta", "alpha"]
    # dependentRequired values sorted as string sets
    assert gadget["dependentRequired"]["name"] == ["desc", "label"]
    # $defs recurse into schema — enum and examples sorted
    mode = gadget["$defs"]["mode"]
    assert mode["enum"] == ["off", "on"]
    assert mode["examples"] == ["off", "on"]
