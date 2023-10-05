import nix

from nut.nut_safe_nix_value import safe_nix_attr_get
from nut.nut_base import NutBase, NutTestId


class NutNodeError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutNode(NutBase):
    message: str
    id: NutTestId

    def __init__(self, nix_value: nix.expr.Value, nut_test_id: NutTestId, depth: int):
        super().__init__(nix_value, depth)

        if self.id != nut_test_id:
            raise NutNodeError(
                f"Incorrect test identifier found, expected {nut_test_id}, got {self.id}"
            )

        message = safe_nix_attr_get(self.result, "message")

        if message is None:
            raise NutNodeError(
                f"Could not find key message under attrset {self.result}"
            )

        if message.success is False:
            raise NutNodeError(
                f"Evaluation for nix value under message on attrset {self.result} failed!"
            )

        if message.type is not nix.expr.Type.string:
            raise NutNodeError(
                f'Expected value under key "message" on attrset {self.result} to be of type string'
            )

        self.message = message.result

    def __repr__(self):
        gap = self.spaces + self.offset
        return f"\n{gap}message: {self.message}\n{gap}id: {self.id}\n{gap}depth: {self.depth}\n{gap}result: {self.result}\n{gap}value:"
