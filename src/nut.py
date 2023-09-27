import nix
import click
import sys
from pathlib import Path


class NutTestError(Exception):
    """Raised for errors in the application's logic."""

    pass


def get_nut_root_from_target_flake_output(tfo_nix_val):
    """ """


@click.command()
@click.argument(
    "flake_ref",
    type=click.STRING,
    default=".",
)
def exec_args(flake_ref):
    """
    Lets do some nutty testing

    [FLAKE_DIR] by default will be the current directory if no argument is specified
    """

    relative_flake_path = None
    target_flake_output = None

    if "#" not in flake_ref:
        relative_flake_path = flake_ref
        target_flake_output = "test"
    else:
        (relative_flake_path, target_flake_output) = flake_ref.split("#")

    flake_path = str((Path(relative_flake_path)).absolute())

    print(flake_path)
    print(target_flake_output)

    flake = nix.eval("builtins.getFlake")(flake_path).force()
    test = flake.get(target_flake_output).force()  # .force().get(target_flake_output)
    print(test)

    # flake_output_keys = flake.force().keys()

    # if flake.force().get("test") is None:
    #     raise NutTestError("Could not find test attribute in flake output attrset")

    # if file_path.is_file():
    #     print(f"The file 'flake.nix' exists in {directory}")
    # else:
    #     print(f"The file {filename} does not exist in {directory}")
    # if ctx is None:
    #     raise click.UsageError("No flake path passed as argument", None)
    # print(flake)
    # if os.path.join(flake, "flake.nix"):
    #     null
    # else:
    # click.echo(click.format_filename(flake))


if __name__ == "__main__":
    exec_args()
