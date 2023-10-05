from __future__ import annotations

from typing import Dict, Literal, TypeAlias, Union
import nix
from nut.nut_safe_nix_value import safe_nix_attr_get, safe_nix_value


class NutBaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


NutTestId: TypeAlias = Union[
    Literal["__test_root__"],
    Literal["__test_branch__"],
    Literal["__test_case__"],
    Literal["__assertion__"],
]


class NutBase:
    result: Dict[str, nix.expr.Value]
    id: str
    depth: int

    def __init__(self, nix_value: nix.expr.Value, depth: int):
        self.nix_value: nix.expr.Value = nix_value
        self.depth = depth

        _value = safe_nix_value(nix_value)

        if _value.success is True:
            if _value.type is nix.expr.Type.attrs:
                self.result = _value.result
            else:
                raise NutBaseError("Value must evaluate to an attrset")
        else:
            raise NutBaseError(
                "Unexpected Evaluation: Could not evaluate nix_value"
            ) from _value.error

        id = safe_nix_attr_get(self.result, "__test__")
        if id is None:
            raise NutBaseError(
                f"Could not find key __test__ under attrset {self.result}"
            )

        if id.success is False:
            raise NutBaseError(
                f"Evaluation for nix value under __test__ on attrset f{self.result} failed!"
            )

        if id.type is not nix.expr.Type.string:
            raise NutBaseError(
                f"Evaluation for nix value under __test__ on attrset f{self.result} failed!"
            )

        self.id = id.result
