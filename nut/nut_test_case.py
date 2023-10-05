from __future__ import annotations

from nut.nut_safe_nix_value import safe_nix_attr_get
from nut.nut_node import NutNode
from nut.nut_assertion import NutAssertion
import nix


class NutTestCaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutTestCase(NutNode):
    def __init__(self, nix_value: nix.expr.Value, depth: int):
        super().__init__(nix_value, "__test_case__", depth)

        v = self.result.get("value")
        if v is None:
            raise NutTestCaseError(
                f'Could not find key "value" under attrs {self.result}'
            )
        else:
            self.value = NutAssertion(v, self.depth + 1)

    def __repr__(self):
        return f"{self.spaces}<NixTestCase {super().__repr__()}\n{self.spaces}{self.spaces}>"
