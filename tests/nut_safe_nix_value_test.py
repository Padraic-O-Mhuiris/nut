from pathlib import PurePath, PurePosixPath
from collections import OrderedDict
from typing import Dict, List, cast
from typing_extensions import assert_never
import unittest
import nix.expr
import nix
import os
from allpairspy import AllPairs
from nut.nut_safe_nix_value import (
    safe_nix_eval,
)


class Test__nut_safe_nix_value(unittest.TestCase):
    def test__safe_nix_eval(self):
        parameters = OrderedDict(
            {
                "inputs": [
                    '"a"',
                    '"wlxqnxnqkwkqkw"',
                    "2",
                    "2.11212",
                    "null",
                    "./../x",
                    "./.",
                    # "/",
                    "/ssss",
                    "true",
                    "false",
                    "1 == 2",
                    "null",
                    "(x: x)",
                    "[]",
                    "[1 2]",
                    "{ a = 3; }",
                    "let s = rec { x = { y = (arg: arg); }; z = (x.y a.b); a = { b = 2.0; }; }; in s.z",
                ],
                "other": [""],
            }
        )
        for test_case in AllPairs(parameters):
            with self.subTest(test_case=test_case):
                input = test_case[0]
                safe_nix_value = safe_nix_eval(input)
                if safe_nix_value.success is True:
                    if safe_nix_value.type is nix.expr.Type.int:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            int,
                            f"Expected inner value: {safe_nix_value.result} to be an int, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.result, int(input))
                        self.assertEqual(safe_nix_value.error, None)

                    elif safe_nix_value.type is nix.expr.Type.float:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            float,
                            f"Expected inner value: {safe_nix_value.result} to be a string, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)

                    elif safe_nix_value.type is nix.expr.Type.string:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            str,
                            f"Expected inner value: {safe_nix_value.result} to be a string, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.result, input[1:-1])
                        self.assertEqual(safe_nix_value.error, None)

                    elif safe_nix_value.type is nix.expr.Type.bool:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            bool,
                            f"Expected inner value: {safe_nix_value.result} to be a bool, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)

                    elif safe_nix_value.type is nix.expr.Type.null:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            type(None),
                            f"Expected inner value: {safe_nix_value.result} to be a None, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.result, None)
                        self.assertEqual(safe_nix_value.error, None)
                    elif safe_nix_value.type is nix.expr.Type.path:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            PurePosixPath,
                            f"Expected inner value: {safe_nix_value.result} to be a PurePosixPath, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(
                            safe_nix_value.result,
                            PurePath(
                                os.path.realpath(
                                    os.path.join(os.path.dirname(__file__), input)
                                )
                            ),
                        )
                        self.assertEqual(safe_nix_value.error, None)
                    elif safe_nix_value.type is nix.expr.Type.function:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            nix.expr.Function,
                            f"Expected inner value: {safe_nix_value.result} to be a Nix Function, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)
                    elif safe_nix_value.type is nix.expr.Type.external:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            nix.expr.ExternalValue,
                            f"Expected inner value: {safe_nix_value.result} to be a Nix ExternalValue, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)
                    elif safe_nix_value.type is nix.expr.Type.attrs:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            Dict,
                            f"Expected inner value: {safe_nix_value.result} to be a Dict, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)
                        for k, v in (cast(Dict, safe_nix_value.result)).items():
                            self.assertIsInstance(k, str)
                            self.assertIsInstance(v, nix.expr.Value)
                    elif safe_nix_value.type is nix.expr.Type.list:
                        self.assertIsInstance(
                            safe_nix_value.result,
                            List,
                            f"Expected inner value: {safe_nix_value.result} to be a List, got: {type(safe_nix_value.result)}",
                        )
                        self.assertEqual(safe_nix_value.error, None)
                        for v in cast(List, safe_nix_value.result):
                            self.assertIsInstance(v, nix.expr.Value)
                    else:
                        assert_never(safe_nix_value)


if __name__ == "__main__":
    unittest.main()
