from __future__ import annotations

from nut.nut_node import NutNode
import nix


class NutTestCase(NutNode):
    # value: NutAssertion

    def __init__(self, nix_value: nix.expr.Value, depth: int):
        super().__init__(nix_value, "__test_case__", depth)

    def __repr__(self):
        return f"<NixTestCase {super().__repr__()}>"
