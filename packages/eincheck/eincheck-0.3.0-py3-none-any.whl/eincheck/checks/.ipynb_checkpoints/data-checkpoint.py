import dataclasses
import functools
import sys
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from eincheck.checks.shapes import check_shapes
from eincheck.parser.dim_spec import ShapeSpec
from eincheck.types import ShapeVariable

_T = TypeVar("_T")


class DataWrapper(ABC):
    module_name: Optional[str] = None

    @classmethod
    def can_load(cls) -> bool:
        return cls.module_name is None or cls.module_name in sys.modules

    @abstractmethod
    def is_match(self, x: Any) -> bool:
        """Whether x is a data object of the right type."""

    @abstractmethod
    def wrap(
        self, cls: _T, shapes: Dict[str, ShapeSpec], bindings: Dict[str, ShapeVariable]
    ) -> _T:
        pass


class NamedTupleWrapper(DataWrapper):
    def is_match(self, x: Any) -> bool:
        return isinstance(x, tuple) and hasattr(x, "_fields")

    def wrap(
        self, cls: _T, shapes: Dict[str, ShapeSpec], bindings: Dict[str, ShapeVariable]
    ) -> _T:
        assert set(cls._fields) >= set(shapes)  # type: ignore[attr-defined]

        _new = cls.__new__

        @functools.wraps(_new)  # type: ignore[misc]
        @classmethod
        def new_new(cls: Any, *a: Any, **k: Any) -> Any:
            out = _new(*a, **k)

            check_shapes(
                **{k: (getattr(out, k), s) for k, s in shapes.items()},
                **bindings,
            )
            return out

        cls.__new__ = new_new  # type: ignore[assignment]

        return cls


def _func_with_check(
    cls: Any,
    func: str,
    shapes: Dict[str, ShapeSpec],
    bindings: Dict[str, ShapeVariable],
    append: bool,
) -> None:
    old_f = getattr(cls, func)

    if append:

        def new_f(self: Any, *a: Any, **k: Any) -> Any:
            old_f(self, *a, **k)
            check_shapes(
                **{k: (getattr(self, k), s) for k, s in shapes.items()},
                **bindings,
            )

    else:

        def new_f(self: Any, *a: Any, **k: Any) -> Any:
            check_shapes(
                **{k: (getattr(self, k), s) for k, s in shapes.items()},
                **bindings,
            )
            old_f(self, *a, **k)

    new_f = functools.wraps(old_f)(new_f)

    setattr(cls, func, new_f)


class DataclassWrapper(DataWrapper):
    def is_match(self, x: Any) -> bool:
        return dataclasses.is_dataclass(x)

    def wrap(
        self, cls: _T, shapes: Dict[str, ShapeSpec], bindings: Dict[str, ShapeVariable]
    ) -> _T:
        assert {f.name for f in dataclasses.fields(cls)} >= set(shapes)

        if hasattr(cls, "__post_init__"):
            _func_with_check(cls, "__post_init__", shapes, bindings, False)
        else:
            _func_with_check(cls, "__init__", shapes, bindings, True)
        return cls


class AttrsWrapper(DataWrapper):
    module_name = "attrs"

    def __init__(self) -> None:
        super().__init__()
        import attrs

        self.attrs = attrs

    def is_match(self, x: Any) -> bool:
        return self.attrs.has(x)

    def wrap(
        self, cls: _T, shapes: Dict[str, ShapeSpec], bindings: Dict[str, ShapeVariable]
    ) -> _T:
        assert {a.name for a in attrs.fields(cls)} >= set(shapes)  # type: ignore[arg-type]

        if hasattr(cls, "__attrs_post_init__"):
            _func_with_check(cls, "__attrs_post_init__", shapes, bindings, False)

        else:
            _func_with_check(cls, "__init__", shapes, bindings, True)

        return cls


_wrappers: List[DataWrapper] = []

_T_Data = TypeVar("_T_Data")


def check_data(**kwargs: Union[str, int]) -> Callable[[_T_Data], _T_Data]:
    bindings: Dict[str, ShapeVariable] = {
        k: v for k, v in kwargs.items() if isinstance(v, (int, tuple))
    }
    shapes: Dict[str, ShapeSpec] = {
        k: v for k, v in kwargs.items() if isinstance(v, (str, list))
    }

    def wrapper(cls: _T_Data) -> _T_Data:
        for w in _wrappers:
            if w.is_match(cls):
                return w.wrap(cls, shapes, bindings)

        for w_cls in DataWrapper.__subclasses__():
            if w_cls.can_load:
                _wrappers.append(w_cls())
                if _wrappers[-1].is_match(cls):
                    return _wrappers[-1].is_match(cls, shapes, bindings)

        raise TypeError(f"Unexpected data type {type(cls)}")

    return wrapper
