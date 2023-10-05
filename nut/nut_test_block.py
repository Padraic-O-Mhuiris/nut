from __future__ import annotations

import nix

from nut.nut_node import NutNode
from nut.nut_safe_nix_value import safe_nix_attr_get
from nut.nut_test_case import NutTestCase
from typing import List
from nut.nut_base import NutBase, NutTestId


class NutBranchError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutBranch(NutNode):
    value: List[NutTestBlock | NutTestCase] = []

    def __init__(self, nix_value: nix.expr.Value, nut_test_id: NutTestId, depth: int):
        super().__init__(nix_value, nut_test_id, depth)

        value = safe_nix_attr_get(self.result, "value")

        if value is None:
            raise NutBranchError(
                f'Could not find key "value" under attrset {self.result}'
            )

        if value.success is False:
            raise NutBranchError(
                f'Evaluation for nix value under "value" on attrset {self.result} failed!'
            )

        if value.type is not nix.expr.Type.list:
            raise NutBranchError(
                f'Expected value under key "value" on attrset {self.result} to be of type list'
            )

        for unevaluated_item in value.result:
            item = NutBase(unevaluated_item, 0)

            if item.id == "__test_branch__":
                self.value = self.value + [NutTestBlock(unevaluated_item, depth + 1)]
            elif item.id == "__test_case__":
                self.value = self.value + [NutTestCase(unevaluated_item, depth + 1)]

    def __str__(self):
        inner: str = ""
        for v in self.value:
            if self.id == "__test_branch__":
                inner += f"\n{self.spaces}    {v.__str__()}"
            else:
                inner += f"\n{self.spaces}  {v.__str__()}"

        if self.id == "__test_branch__":
            return f"{super().__str__()}\n{self.spaces}  [{inner}\n{self.spaces}  ]"
        else:
            return f"{super().__str__()}\n{self.spaces}[{inner}\n{self.spaces}]"


class NutTestBlock(NutBranch):
    def __init__(self, nix_value: nix.expr.Value, depth: int):
        super().__init__(nix_value, "__test_branch__", depth)

    def __str__(self):
        return f"<NixTestBlock {super().__str__()}>"
