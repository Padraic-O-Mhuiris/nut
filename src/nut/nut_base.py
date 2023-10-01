import nix

from nut.nut_utils import safe_nix_value_force


class NutBaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutBase:
    def __init__(self, nix_value: nix.expr.Value):
        self.nix_value: nix.expr.Value = nix_value
        (result, exception, success) = safe_nix_value_force(nix_value)
        if success:
            self.value: nix.expr.Evaluated = result
        else:
            raise NutBaseError(
                "Unexpected Evaluation: Could not evaluate nix_value"
            ) from exception
