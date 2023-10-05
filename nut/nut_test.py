from __future__ import annotations

import nix

from nut.nut_test_block import NutBranch


class NutTestError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutTest(NutBranch):
    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__test_root__", 0)

    def __str__(self):
        return f"<NixTest {super().__str__()}>"

    # def __repr__(self):
    #     return super().__repr__()
