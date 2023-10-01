import nix
import nix.store


class NutTestError(Exception):
    """Raised for errors in the application's testing logic"""

    pass


def nix_value_from_python(
    v: nix.expr.Evaluated | nix.expr.DeepEvaluated,
) -> nix.expr.Value:
    try:
        return nix.expr.State([], nix.store.Store()).val_from_python(v)
    except Exception as e:
        raise NutTestError("Nix Value construction failed!") from e
