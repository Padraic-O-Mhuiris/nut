from __future__ import annotations

from nut.nut_base import NutBase
import nix


class NutAssertion(NutBase):
    def __init__(self, nix_value: nix.expr.Value, depth: int):
        super().__init__(nix_value, depth)

    def __repr__(self):
        return "<NixAssertion>"
