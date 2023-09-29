import nix

def safe_nix_value_force(
    nix_value: nix.expr.Value,
) -> tuple[nix.expr.Evaluated | None, bool]:
    try:
        return (nix_value.force(), True)
    except as e:
        return (None, False)
