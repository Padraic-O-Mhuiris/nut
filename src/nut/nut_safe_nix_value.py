import nix
import nix.expr
import nix.store
import os
import inspect
from typing import TypeAlias, Literal, Dict, List, Union, cast
from typing_extensions import assert_never
from pathlib import PurePath
from dataclasses import dataclass


@dataclass
class SafeNixBase:
    result: nix.expr.Evaluated
    type: nix.expr.Type
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixError:
    error: Exception
    result: None = None
    type: None = None
    success: Literal[False] = False


@dataclass
class SafeNixString:
    result: str
    type: Literal[nix.expr.Type.string] = nix.expr.Type.string
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixBool:
    result: bool
    type: Literal[nix.expr.Type.bool] = nix.expr.Type.bool
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixInt:
    result: int
    type: Literal[nix.expr.Type.int] = nix.expr.Type.int
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixFloat:
    result: float
    type: Literal[nix.expr.Type.float] = nix.expr.Type.float
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixNull:
    result: None = None
    type: Literal[nix.expr.Type.null] = nix.expr.Type.null
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixPath:
    result: PurePath
    type: Literal[nix.expr.Type.path] = nix.expr.Type.path
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixFunction:
    result: nix.expr.Function
    type: Literal[nix.expr.Type.function] = nix.expr.Type.function
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixExternal:
    result: nix.expr.ExternalValue
    type: Literal[nix.expr.Type.external] = nix.expr.Type.external
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixAttrs:
    result: Dict[str, nix.expr.Value]
    type: Literal[nix.expr.Type.attrs] = nix.expr.Type.attrs
    error: None = None
    success: Literal[True] = True


@dataclass
class SafeNixList:
    result: List[nix.expr.Value]
    type: Literal[nix.expr.Type.list] = nix.expr.Type.list
    error: None = None
    success: Literal[True] = True


SafeNixValue: TypeAlias = Union[
    SafeNixError,
    SafeNixInt,
    SafeNixBool,
    SafeNixString,
    SafeNixFloat,
    SafeNixNull,
    SafeNixPath,
    SafeNixFunction,
    SafeNixExternal,
    SafeNixAttrs,
    SafeNixList,
]


def safe_nix_value(nix_value: nix.expr.Value) -> SafeNixValue:
    try:
        nix_value_type: nix.expr.Type = nix_value.get_type()
        evaluated_nix_value: nix.expr.Evaluated = nix_value.force(
            nix.expr.evaluated_types, False  # Avoids deep evaluation!
        )

        match nix_value_type:
            case nix.expr.Type.int:
                return SafeNixInt(result=cast(int, evaluated_nix_value))
            case nix.expr.Type.float:
                return SafeNixFloat(result=cast(float, evaluated_nix_value))
            case nix.expr.Type.bool:
                return SafeNixBool(result=cast(bool, evaluated_nix_value))
            case nix.expr.Type.string:
                return SafeNixString(result=cast(str, evaluated_nix_value))
            case nix.expr.Type.null:
                return SafeNixNull(result=cast(None, evaluated_nix_value))
            case nix.expr.Type.path:
                return SafeNixPath(result=cast(PurePath, evaluated_nix_value))
            case nix.expr.Type.function:
                return SafeNixFunction(
                    result=cast(nix.expr.Function, evaluated_nix_value)
                )
            case nix.expr.Type.external:
                return SafeNixExternal(
                    result=cast(nix.expr.ExternalValue, evaluated_nix_value)
                )
            case nix.expr.Type.attrs:
                return SafeNixAttrs(
                    result=cast(Dict[str, nix.expr.Value], evaluated_nix_value)
                )
            case nix.expr.Type.list:
                return SafeNixList(
                    result=cast(List[nix.expr.Value], evaluated_nix_value)
                )
            case _:
                return assert_never()

    except Exception as e:
        return SafeNixError(error=e)


def safe_nix_eval(value: str) -> SafeNixValue:

    frame = inspect.stack()[1]
    file_name = frame.filename
    absolute_file_path = os.path.realpath(file_name)
    directory = os.path.dirname(absolute_file_path)

    return safe_nix_value(nix.eval(value, directory))
