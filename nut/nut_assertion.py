from nut.nut_base import NutBase
import nix


class NutAssertion(NutBase):
    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__assertion__")
