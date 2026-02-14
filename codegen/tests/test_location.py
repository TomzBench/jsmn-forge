import pytest
from jsmn_forge.spec.location import ROOT, Location


class TestToPointer:
    def test_empty(self) -> None:
        assert Location().to_pointer() == ""

    def test_simple(self) -> None:
        loc = Location(("components", "schemas", "widget"))
        assert loc.to_pointer() == "/components/schemas/widget"

    def test_escape_slash(self) -> None:
        loc = Location(("paths", "/items", "get"))
        assert loc.to_pointer() == "/paths/~1items/get"

    def test_escape_tilde(self) -> None:
        loc = Location(("a~b",))
        assert loc.to_pointer() == "/a~0b"

    def test_escape_both(self) -> None:
        loc = Location(("a~/b",))
        assert loc.to_pointer() == "/a~0~1b"


class TestFromPointer:
    def test_empty(self) -> None:
        assert Location.from_pointer("") == Location()

    def test_root(self) -> None:
        assert Location.from_pointer("/") == Location()

    def test_simple(self) -> None:
        loc = Location.from_pointer("/components/schemas/widget")
        assert loc == ("components", "schemas", "widget")

    def test_unescape_slash(self) -> None:
        loc = Location.from_pointer("/paths/~1items/get")
        assert loc == ("paths", "/items", "get")

    def test_unescape_tilde(self) -> None:
        loc = Location.from_pointer("/a~0b")
        assert loc == ("a~b",)

    def test_unescape_both(self) -> None:
        loc = Location.from_pointer("/a~0~1b")
        assert loc == ("a~/b",)


class TestRoundTrip:
    @pytest.mark.parametrize(
        "segments",
        [
            (),
            ("components", "schemas", "widget"),
            ("paths", "/items", "get"),
            ("a~b",),
            ("a~/b",),
            ("paths", "/items/{id}", "get", "responses", "200"),
        ],
    )
    def test_roundtrip(self, segments: tuple[str, ...]) -> None:
        loc = Location(segments)
        assert Location.from_pointer(loc.to_pointer()) == loc


class TestPush:
    def test_push_returns_location(self) -> None:
        loc = Location(("a", "b"))
        child = loc.push("c")
        assert isinstance(child, Location)
        assert child == ("a", "b", "c")

    def test_push_does_not_mutate(self) -> None:
        loc = Location(("a",))
        loc.push("b")
        assert loc == ("a",)

    def test_push_from_root(self) -> None:
        child = ROOT.push("components")
        assert child == ("components",)
        assert isinstance(child, Location)

    def test_push_chain(self) -> None:
        loc = Location(("a",)).push("b").push("c")
        assert loc == ("a", "b", "c")


class TestTupleCompat:
    def test_indexing(self) -> None:
        loc = Location(("a", "b", "c"))
        assert loc[0] == "a"
        assert loc[-1] == "c"

    def test_len(self) -> None:
        assert len(Location(("a", "b"))) == 2

    def test_iteration(self) -> None:
        assert list(Location(("a", "b"))) == ["a", "b"]

    def test_hashable(self) -> None:
        loc = Location(("a", "b"))
        d: dict[tuple[str, ...], str] = {loc: "value"}
        assert d[("a", "b")] == "value"

    def test_unpack_extend(self) -> None:
        loc = Location(("a", "b"))
        extended = (*loc, "c")
        assert extended == ("a", "b", "c")

    def test_equality_with_tuple(self) -> None:
        assert Location(("a", "b")) == ("a", "b")
