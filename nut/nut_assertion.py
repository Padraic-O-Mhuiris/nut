from __future__ import annotations

from typing import Literal, cast
from nut.nut_base import NutBase
import nix

from nut.nut_safe_nix_value import SafeNixError, SafeNixValue, safe_nix_attr_get


class NutAssertionError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutAssertion(NutBase):
    left: SafeNixValue | SafeNixError
    right: SafeNixValue | SafeNixError
    type: Literal["EQUALS"]

    def __init__(self, nix_value: nix.expr.Value, depth: int):
        super().__init__(nix_value, depth)

        left_value = safe_nix_attr_get(self.result, "left")
        if left_value is None:
            raise NutAssertionError(
                f'Could not find key "left" under attrs {self.result}'
            )
        self.left = left_value

        right_value = safe_nix_attr_get(self.result, "right")
        if right_value is None:
            raise NutAssertionError(
                f'Could not find key "right" under attrs {self.result}'
            )
        self.right = right_value

        type_value = safe_nix_attr_get(self.result, "type")
        if type_value is None:
            raise NutAssertionError(
                f'Could not find key "type" under attrs {self.result}'
            )

        # TODO Expand to a check in list
        if type_value.result != "EQUALS":
            raise NutAssertionError(
                f'Could not find key "type" under attrs {self.result}'
            )

        self.type = cast(Literal["EQUALS"], type_value.result)

    def __repr__(self):
        return f"<NixAssertion\n{self.spaces}{self.offset}result: {self.result}\n{self.spaces}{self.offset}type: {self.type}\n{self.spaces}{self.offset}left: {self.left}\n{self.spaces}{self.offset}right: {self.right}\n{self.spaces}{self.spaces}>"
