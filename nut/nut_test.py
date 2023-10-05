from __future__ import annotations

from typing import List

import nix
from nut.nut_base import NutNode
from nut.nut_test_block import NutTestBlock
from nut.nut_test_case import NutTestCase


class NutTestError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutTest(NutNode):
    value: List[NutTestBlock | NutTestCase]

    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__test_root__")
