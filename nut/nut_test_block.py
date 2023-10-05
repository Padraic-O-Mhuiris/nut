from __future__ import annotations

from typing import List
from nut.nut_base import NutNode
from nut.nut_test_case import NutTestCase
import nix


class NutTestBlock(NutNode):
    value: List[NutTestBlock | NutTestCase]

    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__test_branch__")
