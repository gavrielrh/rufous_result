from abc import ABC
from dataclasses import dataclass
from typing import Callable, Generic, Iterator, Optional, TypeVar, Union

# Generic types
T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = Callable[[T], U]
D = Callable[[E], U]
O = Callable[[E], F]


@dataclass
class Result(Generic[T, E]):
    value: Union[T, E]

    def is_ok(self) -> bool:
        raise NotImplementedError

    def is_err(self) -> bool:
        raise NotImplementedError

    def ok(self) -> Optional["Ok"]:
        raise NotImplementedError

    def err(self) -> Optional["Err"]:
        raise NotImplementedError

    def map(self, op: F) -> "Result[U, E]":
        raise NotImplementedError

    def map_or(self, default: U, f: F) -> U:
        raise NotImplementedError

    def map_or_else(self, default: D, f: F) -> U:
        raise NotImplementedError

    def map_err(self, op: O) -> "Result[T, F]":
        raise NotImplementedError

    def iter(self) -> Iterator[Optional[T]]:
        raise NotImplementedError

    def expect(self, msg: str) -> T:
        raise NotImplementedError

    def unwrap(self) -> T:
        raise NotImplementedError

    def unwrap_or_default(self) -> T:
        raise NotImplementedError

    def expect_err(self, msg: str) -> E:
        raise NotImplementedError

    def unwrap_err(self) -> E:
        raise NotImplementedError

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        raise NotImplementedError

    def and_then(self, op: F) -> "Result[U, E]":
        raise NotImplementedError

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        raise NotImplementedError

    def or_else(self, op: O) -> "Result[T, F]":
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    def unwrap_or_else(self, op: F) -> T:
        raise NotImplementedError


@dataclass
class Ok(Result):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> Optional["Ok"]:
        return self.value

    def err(self) -> Optional["Err"]:
        return None

    def map(self, op: F) -> "Result[U, E]":
        return Ok(op(self.value))

    def map_or(self, default: U, f: F) -> U:
        return f(self.value)

    def map_or_else(self, default: D, f: F) -> U:
        return f(self.value)

    def map_err(self, op: O) -> "Result[T, F]":
        return self

    def iter(self) -> Iterator[Optional[T]]:
        yield self.value

    def expect(self, msg: str) -> T:
        return self.value

    def unwrap(self) -> T:
        return self.value

    def unwrap_or_default(self) -> T:
        return self.value

    def expect_err(self, msg: str) -> E:
        raise RuntimeError(f"{msg}: {self.value}")

    def unwrap_err(self) -> E:
        raise RuntimeError(f"{self.value}")

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        if res.is_err():
            return res
        return res

    def and_then(self, op: F) -> "Result[U, E]":
        return op(self.value)

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        return self

    def or_else(self, op: O) -> "Result[T, F]":
        return self

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, op: F) -> T:
        return self.value


@dataclass
class Err(Result):
    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> Optional[Ok]:
        return None

    def err(self) -> Optional["Err"]:
        return self.value

    def map(self, op: F) -> "Result[U, E]":
        return self

    def map_or(self, default: U, f: F) -> U:
        return default

    def map_or_else(self, default: D, f: F) -> U:
        return default(self.value)

    def map_err(self, op: O) -> "Result[T, F]":
        return Err(op(self.value))

    def iter(self) -> Iterator[Optional[T]]:
        yield None

    def expect(self, msg: str) -> T:
        raise RuntimeError(f"{msg}: {self.value}")

    def unwrap(self) -> T:
        raise RuntimeError(self.value)

    def unwrap_or_default(self) -> T:
        c = self.value.__class__
        try:
            return c()
        except:
            raise RuntimeError(f"Cannot provide default value for: {c}")

    def expect_err(self, msg: str) -> E:
        return self.value

    def unwrap_err(self) -> E:
        return self.value

    def re_and(self, res: "Result[U, E]") -> "Result[U, E]":
        return self

    def and_then(self, op: F) -> "Result[U, E]":
        return self

    def re_or(self, res: "Result[T, F]") -> "Result[T, F]":
        return res

    def or_else(self, op: O) -> "Result[T, F]":
        return op(self.value)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: F) -> T:
        return op(self.value)
