from dataclasses import dataclass
from typing import Iterator, TypeVar, Generic, Optional, Callable, Union, get_args

# Generic types
T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')
F = Callable[[T], U]
D = Callable[[E], U]
O = Callable[[E], F]

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    value: E

@dataclass
class Result(Generic[T,E]):
    value: Union[Ok[T], Err[E]]
    
    def is_ok(self) -> bool:
        return isinstance(self.value, Ok)

    def is_err(self) -> bool:
        return isinstance(self.value, Err)

    def ok(self) -> Optional[Ok]:
        if self.is_ok():
            return self.value
        return None

    def err(self) -> Optional[Err]:
        if self.is_err():
            return self.value
        return None

    def map(self, op: F) -> 'Result[U, E]':
        new_value = self.value
        if self.is_ok():
            new_value = op(self.value)
        return Result(new_value)
    
    def map_or(self, default: U, f: F) -> U:
        if self.is_ok():
            return f(self.value)
        return default
    
    def map_or_else(self, default: D, f: F) -> U:
        if self.is_ok():
            return f(self.value)
        return default(self.value)

    def map_err(self, op: O) -> 'Result[T, F]':
        if self.is_err():
            return Result(Err(op(self.value.value)))
        return self

    def iter(self) -> Iterator[T]:
        if self.is_ok():
            yield self.value.value
        yield None
    
    def expect(self, msg: str) -> T:
        if self.is_ok():
            return self.value.value
        raise RuntimeError(f"{msg}: {self.value.value}")
    
    def unwrap(self) -> T:
        if self.is_ok():
            return self.value.value
        raise RuntimeError(self.value.value)

    def unwrap_or_default(self) -> T:
        # @TODO Holding off on implementing this
        # until I understand Python types better
        raise NotImplementedError

    def expect_err(self, msg: str) -> E:
        if self.is_err():
            return self.value.value
        raise RuntimeError(f"{msg}: {self.value.value}")
    
    def unwrap_err(self) -> E:
        if self.is_err():
            return self.value.value
        raise RuntimeError(f"{self.value.value}")
    
    def x_and(self, res: 'Result[U, E]') -> 'Result[U, E]':
        if self.is_err():
            return self
        if res.is_err():
            return res
        return res
    
    def and_then(self, op: F) -> 'Result[U, E]':
        pass 