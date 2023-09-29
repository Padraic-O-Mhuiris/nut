import nix
import click
import sys
from pathlib import Path
from functools import reduce

from rich.tree import Tree
from rich import print


class NutTestError(Exception):
    """Raised for errors in the application's logic."""

    pass


def eval_equals_assertion(assertion_block, display_tree):
    """"""
    print(assertion_block)

    left = assertion_block["left"]
    right = assertion_block["right"]

    left_type = type(left.get_type())
    right_type = type(right.get_type())

    print(left)
    print(right)

    # return (left.force(), right.force(), dir(left_type), right_type)


def eval_assertion(assertion_block, display_tree):
    """"""
    assertion_type = assertion_block["type"].force()

    if assertion_type == "EQUALS":
        return eval_equals_assertion(assertion_block, display_tree)
    else:
        display_tree.add("Unsupported assertion type")

    return 1


def run_tests(_test_tree, display_tree):
    """"""
    test_tree = _test_tree.force()

    def run_test_block(acc, _node):
        node = _node.force()
        node_type = node["__test__"].force()
        node_id = node["id"].force()
        node_message = node["message"].force()
        node_value = node["value"].force()

        display_string = f"{node_message}"

        if node_type == "__test_branch__":
            return acc | {(node_id): run_tests(_node, display_tree.add(display_string))}
        else:
            return acc | {
                (node_id): eval_assertion(node_value, display_tree.add(display_string))
            }

    return reduce(run_test_block, test_tree["value"].force(), {})


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

    flake = nix.eval("builtins.getFlake")(flake_path).force()
    test_tree = flake.get(target_flake_output)  # .force().get(target_flake_output)

    # print(test_tree.force())
    test_tree_message = test_tree.force()["message"]

    display_tree = Tree(f"Test: {test_tree_message}")
    t = run_tests(test_tree, display_tree)

    print(t)
    print(display_tree)


# print(test_tree.force())
# print(test_tree_map(lambda x: x, test_tree))

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
