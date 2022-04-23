import pytest

from rufous_result.result import Err, Ok


def test_is_ok():
    x = Ok(-3)
    assert x.is_ok() is True
    x = Err("Some error message")
    assert x.is_ok() is False


def test_is_err():
    x = Ok(-3)
    assert x.is_err() is False
    x = Err("Some error message")
    assert x.is_err() is True


def test_map():
    def _doubler(x):
        return x * 2

    x = Ok(-3)
    assert x.map(_doubler).value == -6
    x = Err("Some error message")
    assert x.map(_doubler) == x


def test_map_or():
    x = Ok("foo")

    def _len(x):
        return len(x)

    default = 42
    assert x.map_or(default, _len) == 3
    x = Err("Some error message")
    assert x.map_or(default, _len) == 42


def test_map_or_else():
    k = 21

    def _len(x) -> int:
        return len(x)

    def _default(x) -> int:
        return k * 2

    x = Ok("foo")
    assert x.map_or_else(_default, _len) == 3
    x = Err("bar")
    assert x.map_or_else(_default, _len) == 42


def test_map_err():
    def _stringify(x: int) -> str:
        return f"error code: {x}"

    x = Ok(2)
    assert x.map_err(_stringify) == x
    x = Err(13)
    expected = Err("error code: 13")
    res = x.map_err(_stringify)
    assert expected == res


def test_iter():
    x = Ok(7)
    x_iter = x.iter()
    assert next(x_iter) == 7
    x = Err("nothing!")
    x_iter = x.iter()
    assert next(x_iter) == None


def test_expect():
    x = Ok("this is fine")
    assert x.expect("Shouldn't raise") == "this is fine"
    x = Err("emergency failure")
    with pytest.raises(RuntimeError) as excinfo:
        x.expect("Testing expect")
        assert "Testing expect: emergency failure" == excinfo.value


def test_unwrap():
    x = Ok(2)
    assert x.unwrap() == 2
    x = Err("emergency failure")
    with pytest.raises(RuntimeError) as excinfo:
        x.unwrap()
        assert "emergency failure" == excinfo.value


def test_unwrap_or_default():
    # Numeric types
    x = Err(42)
    assert x.unwrap_or_default() == 0
    x = Err(3.14)
    assert x.unwrap_or_default() == 0.0
    x = Err(complex(7, 1))
    assert x.unwrap_or_default() == 0
    # Sequence types
    x = Err([1, 4, 5])
    assert x.unwrap_or_default() == []
    x = Err((2, 7))
    assert x.unwrap_or_default() == ()
    # Text sequence types
    x = Err("Yep")
    assert x.unwrap_or_default() == ""
    # Binary sequence types
    x = Err(b"some bytes")
    assert x.unwrap_or_default() == b""
    x = Err(bytearray(10))
    assert x.unwrap_or_default() == bytearray()
    # Set types
    x = Err(set(["jack", "sjoerd"]))
    assert x.unwrap_or_default() == set()
    x = Err(frozenset([2, 4, 6]))
    assert x.unwrap_or_default() == frozenset()
    # Mapping types
    x = Err({"jack": 4098, "sjoerd": 4127})
    assert x.unwrap_or_default() == {}


def test_expect_err():
    x = Ok(10)
    with pytest.raises(RuntimeError) as excinfo:
        x.expect_err("Testing expect_err")
        assert "Testing expect_err: 10" == excinfo.value
    x = Err("It works")
    x.expect_err("It doesn't work") == "It works"


def test_unwrap_err():
    x = Ok(2)
    with pytest.raises(RuntimeError) as excinfo:
        x.unwrap_err()
        assert excinfo.value == "2"
    x = Err("It works")
    x.unwrap_err() == "It works"


def test_re_and():
    x = Ok(2)
    y = Err("late error")
    assert x.re_and(y) == Err("late error")
    x = Err("early error")
    y = Ok("foo")
    assert x.re_and(y) == Err("early error")
    x = Err("not a 2")
    y = Err("late error")
    assert x.re_and(y) == Err("not a 2")
    x = Ok(2)
    y = Ok("different result type")
    assert x.re_and(y) == Ok("different result type")


def test_and_then():
    FAKE_MAX_INT = 1000

    def sq_then_to_str(x):
        if x > FAKE_MAX_INT:
            return Err("overflowed")
        return Ok(f"{x*x}")

    assert Ok(2).and_then(sq_then_to_str) == Ok("4")
    assert Ok(10000).and_then(sq_then_to_str) == Err("overflowed")
    assert Err("not a number").and_then(sq_then_to_str) == Err("not a number")


def test_re_or():
    x = Ok(2)
    y = Err("late error")
    assert x.re_or(y) == Ok(2)
    x = Err("early error")
    y = Ok(2)
    assert x.re_or(y) == Ok(2)
    x = Err("not a 2")
    y = Err("late error")
    assert x.re_or(y) == Err("late error")
    x = Ok(2)
    y = Ok(100)
    assert x.re_or(y) == Ok(2)


def test_or_else():
    def sq(x):
        return Ok(x * x)

    def err(x):
        return Err(x)

    assert Ok(2).or_else(sq).or_else(sq) == Ok(2)
    assert Ok(2).or_else(err).or_else(sq) == Ok(2)
    assert Err(3).or_else(sq).or_else(err) == Ok(9)
    assert Err(3).or_else(err).or_else(err) == Err(3)


def test_unwrap_or():
    default = 2
    x = Ok(9)
    assert x.unwrap_or(default) == 9
    x = Err("error")
    assert x.unwrap_or(default) == default


def test_unwrap_or_else():
    def count(x):
        return len(x)

    assert Ok(2).unwrap_or_else(count) == 2
    assert Err("foo").unwrap_or_else(count) == 3
