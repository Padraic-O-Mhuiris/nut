import nix
from nut.nut_safe_nix_value import safe_nix_value


class NutBaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutBase:
    def __init__(self, nix_value: nix.expr.Value):
        self.nix_value: nix.expr.Value = nix_value
        _value = safe_nix_value(nix_value)

        if _value.success is True:
            self.value = _value.result
            self.type = _value.type
        else:
            raise NutBaseError(
                "Unexpected Evaluation: Could not evaluate nix_value"
            ) from _value.error
