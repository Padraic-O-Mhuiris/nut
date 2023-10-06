from __future__ import annotations

import nix

from nut.nut_test_block import NutBranch

from rich.tree import Tree
from rich import print


class NutTestError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutTest(NutBranch):
    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__test_root__", 0)

    def __repr__(self):
        return f"<NixTest {super().__repr__()}\n>"

    def run(self):
        tree = Tree(f"{self.message}")
        for t in self.value:
            t.run(tree)

        print(tree)
