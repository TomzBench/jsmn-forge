import json


def sort_set(arr: list) -> list:
    """Canonical sort for set-like arrays. Handles primitives, objects, mixed types.
    For: required, enum, type, tags, examples, allOf, oneOf, anyOf, security."""
    return sorted(arr, key=lambda v: json.dumps(v, sort_keys=True))


def sort_set_by(arr: list[dict], *keys: str) -> list[dict]:
    """Sort object arrays by identity key fields.
    For: parameters (name, in)."""
    return sorted(arr, key=lambda x: tuple(x.get(k, "") for k in keys))
