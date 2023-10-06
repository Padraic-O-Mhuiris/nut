import click

from typing import Dict, cast
from pathlib import Path
import nix
import nix.expr
from rich import print

from nut.nut_test import NutTest


def get_flake_attr(relative_path: str, target_flake_attr: str) -> nix.expr.Value:
    flake_path = str((Path(relative_path)).absolute())
    # TODO use safe_nix_eval here
    flake = nix.eval("builtins.getFlake")(flake_path).force()
    assert isinstance(flake, dict), "path to flake did not evaluate to an attrset"
    target_attr = cast(Dict[str, nix.expr.Value], flake).get(target_flake_attr)
    assert (
        target_attr is not None
    ), f"flake attribute: {target_flake_attr} was not found at flake path: {flake_path}"
    return target_attr


@click.command()
@click.argument(
    "flake_ref",
    type=click.STRING,
    default=".",
)
def main(flake_ref: str):
    """
    Lets do some nutty testing

    [FLAKE_DIR] by default will be the current directory if no argument is specified
    """

    if "#" not in flake_ref:
        relative_flake_path = flake_ref
        target_flake_attr = "test"
    else:
        (relative_flake_path, target_flake_attr) = flake_ref.split("#")

    test_attr = get_flake_attr(relative_flake_path, target_flake_attr)
    print(str(NutTest(test_attr)))
    NutTest(test_attr).run()


if __name__ == "__main__":
    main()
