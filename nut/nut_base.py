from typing import Dict, Literal, TypeAlias, Union
import nix
from nut.nut_safe_nix_value import safe_nix_attr_get, safe_nix_value


class NutBaseError(Exception):
    """Raised for errors in the application's logic."""

    pass


NutTestId: TypeAlias = Union[
    Literal["__test_root__"],
    Literal["__test_branch__"],
    Literal["__test_case__"],
    Literal["__assertion__"],
]


class NutBase:
    result: Dict[str, nix.expr.Value]
    id: NutTestId

    def __init__(self, nix_value: nix.expr.Value, nut_test_id: NutTestId):
        self.nix_value: nix.expr.Value = nix_value
        _value = safe_nix_value(nix_value)

        if _value.success is True:
            if _value.type is nix.expr.Type.attrs:
                self.result = _value.result
            else:
                raise NutBaseError("Value must evaluate to an attrset")
        else:
            raise NutBaseError(
                "Unexpected Evaluation: Could not evaluate nix_value"
            ) from _value.error

        id = safe_nix_attr_get(self.result, "__test__")
        if id is None:
            raise NutBaseError(
                f"Could not find key __test__ under attrset {self.result}"
            )

        if id.success is False:
            raise NutBaseError(
                f"Evaluation for nix value under __test__ on attrset f{self.result} failed!"
            )

        if id.result != nut_test_id:
            raise NutBaseError(
                f"Incorrect test identifier found, expected {nut_test_id}, got {id.result}"
            )
        self.id = nut_test_id

    def __repr__(self):
        return f"<NutBase: {self.id} >"

    def __str__(self):
        return f"id: {self.id}"


class NutNode(NutBase):
    message: str

    def __init__(self, nix_value: nix.expr.Value, nut_test_id: NutTestId):
        super().__init__(nix_value, nut_test_id)

        message = safe_nix_attr_get(self.result, "message")

        if message is None:
            raise NutBaseError(
                f"Could not find key message under attrset {self.result}"
            )

        if message.success is False:
            raise NutBaseError(
                f"Evaluation for nix value under message on attrset {self.result} failed!"
            )

        if message.type is not nix.expr.Type.string:
            raise NutBaseError(
                f'Expected value under key "message" on attrset {self.result} to be of type string'
            )

        self.message = message.result

    def __repr__(self):
        return f"<NutNode: {self.id} | {self.message}>"

    def __str__(self):
        return f"message: {self.message}\n{super().__str__()}"
