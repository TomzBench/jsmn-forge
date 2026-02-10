from jsmn_forge.diff import diff, Missing, Extra, MissMatch


def test_identical_returns_empty():
    a = {"x": 1, "y": [1, 2]}
    assert diff(a, a) == {}


def test_top_level_missing_and_extra():
    a = {"a": 1}
    b = {"b": 2}
    result = diff(a, b)
    assert result == {
        ("a",): Missing(1),
        ("b",): Extra(2),
    }


def test_top_level_mismatch():
    a = {"a": 1}
    b = {"a": 2}
    result = diff(a, b)
    assert result == {("a",): MissMatch(1, 2)}


def test_nested_dict_diff():
    a = {"info": {"title": "Foo", "version": "1.0"}}
    b = {"info": {"title": "Bar", "version": "1.0"}}
    result = diff(a, b)
    assert result == {("info", "title"): MissMatch("Foo", "Bar")}


def test_nested_dict_missing_key():
    a = {"info": {"title": "Foo", "desc": "hello"}}
    b = {"info": {"title": "Foo"}}
    result = diff(a, b)
    assert result == {("info", "desc"): Missing("hello")}


def test_list_extra_element():
    a = {"tags": ["api"]}
    b = {"tags": ["api", "v2"]}
    result = diff(a, b)
    assert result == {("tags", "1"): Extra("v2")}


def test_list_missing_element():
    a = {"tags": ["api", "v1"]}
    b = {"tags": ["api"]}
    result = diff(a, b)
    assert result == {("tags", "1"): Missing("v1")}


def test_list_of_dicts():
    a = {"params": [{"name": "id", "in": "path"}]}
    b = {"params": [{"name": "id", "in": "query"}]}
    result = diff(a, b)
    assert result == {("params", "0", "in"): MissMatch("path", "query")}


def test_type_mismatch_scalar_vs_dict():
    a = {"x": "string"}
    b = {"x": {"type": "string"}}
    result = diff(a, b)
    assert result == {("x",): MissMatch("string", {"type": "string"})}
