import pytest
from result.result import Result, Ok, Err


def test_is_ok():
    x = Result(Ok(-3))
    assert x.is_ok() is True
    x = Result(Err("Some error message"))
    assert x.is_ok() is False

def test_is_err():
    x = Result(Ok(-3))
    assert x.is_err() is False
    x = Result(Err("Some error message"))
    assert x.is_err() is True

def test_map():
    def _doubler(x):
        return x.value * 2
    x = Result(Ok(-3))
    assert x.map(_doubler).value == -6
    err = Err("Some error message")
    x = Result(err)
    assert x.map(_doubler).value == err

def test_map_or():
    x = Result(Ok("foo"))
    def _len(x):
        return len(x.value)
    default = 42
    assert x.map_or(default, _len) == 3
    x = Result("Some error message")
    assert x.map_or(default, _len) == 42

def test_map_or_else():
    k = 21
    def _len(x) -> int:
        return len(x.value)
    def _default(x) -> int:
        return k * 2
    x = Result(Ok("foo"))
    assert x.map_or_else(_default, _len) == 3
    x = Result(Err("bar"))
    assert x.map_or_else(_default, _len) == 42

def test_map_err():
    def _stringify(x: int) -> str:
        return f"error code: {x}"
    x = Result(Ok(2))
    assert x.map_err(_stringify) == x
    x = Result(Err(13))
    expected = Result(Err("error code: 13"))
    res = x.map_err(_stringify)
    assert expected == res

def test_iter():
    x = Result(Ok(7))
    x_iter = x.iter()
    assert next(x_iter) == 7
    x = Result(Err("nothing!"))
    x_iter = x.iter()
    assert next(x_iter) == None

def test_expect():
    x = Result(Ok('this is fine'))
    assert x.expect("Shouldn't raise") == 'this is fine'
    x = Result(Err("emergency failure"))
    with pytest.raises(RuntimeError) as excinfo:
        x.expect("Testing expect")
        assert "Testing expect: emergency failure" == excinfo.value

def test_unwrap():
    x = Result(Ok(2))
    assert x.unwrap() == 2
    x = Result(Err("emergency failure"))
    with pytest.raises(RuntimeError) as excinfo:
        x.unwrap()
        assert "emergency failure" == excinfo.value

@pytest.mark.xfail
def test_unwrap_or_default():
    x: Result[int] = Result(Err("Yep"))
    assert x.unwrap_or_default() == 0

def test_expect_err():
    x = Result(Ok(10))
    with pytest.raises(RuntimeError) as excinfo:
        x.expect_err("Testing expect_err")
        assert "Testing expect_err: 10" == excinfo.value
    x = Result(Err("It works"))
    x.expect_err("It doesn't work") == "It works"

def test_unwrap_err():
    x = Result(Ok(2))
    with pytest.raises(RuntimeError) as excinfo:
        x.unwrap_err()
        assert excinfo.value == "2"
    x = Result(Err("It works"))
    x.unwrap_err() == "It works"

def test_x_and():
    x = Result(Ok(2))
    y = Result(Err("late error"))
    assert x.x_and(y) == Result(Err("late error"))
    x = Result(Err("early error"))
    y = Result(Ok("foo"))
    assert x.x_and(y) == Result(Err("early error"))
    x = Result(Err("not a 2"))
    y = Result(Err("late error"))
    assert x.x_and(y) == Result(Err("not a 2"))
    x = Result(Ok(2))
    y = Result(Ok("different result type"))
    assert x.x_and(y) == Result(Ok("different result type"))

# def test_and_then():
#     FAKE_MAX_INT = 1000
#     def sq_then_to_str(x):
#         if x.value > FAKE_MAX_INT:
#             return "overflowed"
#         return f"{x*x}"
