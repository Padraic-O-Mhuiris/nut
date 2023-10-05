from nut.nut_base import NutNode
import nix
from nut.nut_assertion import NutAssertion


class NutTestCase(NutNode):
    value: NutAssertion

    def __init__(self, nix_value: nix.expr.Value):
        super().__init__(nix_value, "__test_case__")
