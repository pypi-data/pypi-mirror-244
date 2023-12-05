from __future__ import annotations

from typing import Callable

import pytest

from maybe import Some, SomeNothing, Maybe, Nothing, UnwrapError


def test_some_factories() -> None:
    instance = Some(1)
    assert instance._value == 1
    assert instance.is_some() is True


def test_nothing_factory() -> None:
    instance = Nothing()
    assert instance.is_nothing() is True


def test_eq() -> None:
    assert Some(1) == Some(1)
    assert Nothing() == Nothing()
    assert Some(1) != Nothing()
    assert Some(1) != Some(2)
    assert not (Some(1) != Some(1))
    assert Some(1) != "abc"
    assert Some("0") != Some(0)


def test_hash() -> None:
    assert len({Some(1), Nothing(), Some(1), Nothing()}) == 2
    assert len({Some(1), Some(2)}) == 2
    assert len({Some("a"), Nothing()}) == 2


def test_repr() -> None:
    """
    ``repr()`` returns valid code if the wrapped value's ``repr()`` does as well.
    """
    o = Some(123)
    n = Nothing()

    assert repr(o) == "Some(123)"
    assert o == eval(repr(o))

    assert repr(n) == "Nothing()"
    assert n == eval(repr(n))


def test_some_value() -> None:
    res = Some('haha')
    assert res.some_value == 'haha'


def test_some() -> None:
    res = Some('haha')
    assert res.is_some() is True
    assert res.is_nothing() is False
    assert res.some_value == 'haha'


def test_nothing() -> None:
    res = Nothing()
    assert res.is_some() is False
    assert res.is_nothing() is True


def test_some_method() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.some() == 'yay'
    # TODO(francium): Can this type ignore directive be removed? mypy may fail?
    assert n.some() is None  # type: ignore[func-returns-value]


def test_expect() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.expect('failure') == 'yay'
    with pytest.raises(UnwrapError):
        n.expect('failure')


def test_unwrap() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.unwrap() == 'yay'
    with pytest.raises(UnwrapError):
        n.unwrap()


def test_unwrap_or() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.unwrap_or('some_default') == 'yay'
    assert n.unwrap_or('another_default') == 'another_default'


def test_unwrap_or_else() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.unwrap_or_else(str.upper) == 'yay'
    assert n.unwrap_or_else(lambda: 'default') == 'default'


def test_unwrap_or_raise() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.unwrap_or_raise(ValueError) == 'yay'
    with pytest.raises(ValueError) as exc_info:
        n.unwrap_or_raise(ValueError)
    assert exc_info.value.args == ()


def test_map() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.map(str.upper).some() == 'YAY'
    assert n.map(str.upper).is_nothing()


def test_map_or() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.map_or('hay', str.upper) == 'YAY'
    assert n.map_or('hay', str.upper) == 'hay'


def test_map_or_else() -> None:
    o = Some('yay')
    n = Nothing()
    assert o.map_or_else(lambda: 'hay', str.upper) == 'YAY'
    assert n.map_or_else(lambda: 'hay', str.upper) == 'hay'


def test_and_then() -> None:
    assert Some(2).and_then(sq).and_then(sq).some() == 16
    assert Some(2).and_then(sq).and_then(to_nothing).is_nothing()
    assert Some(2).and_then(to_nothing).and_then(sq).is_nothing()
    assert Nothing().and_then(sq).and_then(sq).is_nothing()

    assert Some(2).and_then(sq_lambda).and_then(sq_lambda).some() == 16
    assert Some(2).and_then(sq_lambda).and_then(to_nothing_lambda).is_nothing()
    assert Some(2).and_then(to_nothing_lambda).and_then(sq_lambda).is_nothing()
    assert Nothing().and_then(sq_lambda).and_then(sq_lambda).is_nothing()


def test_or_else() -> None:
    assert Some(2).or_else(sq).or_else(sq).some() == 2
    assert Some(2).or_else(to_nothing).or_else(sq).some() == 2
    assert Nothing().or_else(lambda: sq(3)).or_else(lambda: to_nothing(2)).some() == 9
    assert Nothing().or_else(lambda: to_nothing(2)).or_else(lambda: to_nothing(2)).is_nothing()

    assert Some(2).or_else(sq_lambda).or_else(sq).some() == 2
    assert Some(2).or_else(to_nothing_lambda).or_else(sq_lambda).some() == 2


def test_isinstance_result_type() -> None:
    o = Some('yay')
    n = Nothing()
    assert isinstance(o, SomeNothing)
    assert isinstance(n, SomeNothing)
    assert not isinstance(1, SomeNothing)


def test_error_context() -> None:
    n = Nothing()
    with pytest.raises(UnwrapError) as exc_info:
        n.unwrap()
    exc = exc_info.value
    assert exc.maybe is n


def test_slots() -> None:
    """
    Some and Nothing have slots, so assigning arbitrary attributes fails.
    """
    o = Some('yay')
    n = Nothing()
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]


def sq(i: int) -> Maybe[int]:
    return Some(i * i)


def to_nothing(_: int) -> Maybe[int]:
    return Nothing()


# Lambda versions of the same functions, just for test/type coverage
sq_lambda: Callable[[int], Maybe[int]] = lambda i: Some(i * i)
to_nothing_lambda: Callable[[int], Maybe[int]] = lambda _: Nothing()
