import nix
from nix.store import Store
from nix.expr import State


def safe_nix_eval(nix_string_value: str) -> tuple[nix.expr.Value | None, bool]:
    """Allows a safe execution context"""
    store = Store()
    state = State([], store)
    nix_value: nix.expr.Value = state.eval_string(nix_string_value, ".")

    return (None, False)


# def safe_nix_eval(nix_string_value: str) -> tuple[nix.expr.Value | None, bool]:
#     """Allows a safe execution context"""
#     store = Store()
#     state = State([], store)
#     nix_value: nix.expr.Value = state.eval_string(nix_string_value, ".")

#     return (None, False)
