import nix


class NutBaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


class NutBase:
    def __init__(self, nix_value: nix.expr.Value):
        self.nix_value: nix.expr.Value = nix_value
        try:
            self.node: nix.expr.Evaluated = nix_value.force()
        except:
            raise NutBaseError("Unexpected Evaluation: Could not evaluate nix_value")
