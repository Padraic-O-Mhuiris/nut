from pathlib import PurePath, PurePosixPath
from collections import OrderedDict
from typing import Dict, List, cast
from typing_extensions import assert_never
import unittest
import nix.expr
import nix
import os
from allpairspy import AllPairs
from nut.nut_safe_nix_value import safe_nix_eval


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
                if safe_nix_value.success:
                    match safe_nix_value.type:
                        case nix.expr.Type.int:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                int,
                                f"Expected inner value: {safe_nix_value.result} to be an int, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.result, int(input))
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.float:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                float,
                                f"Expected inner value: {safe_nix_value.result} to be a string, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.string:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                str,
                                f"Expected inner value: {safe_nix_value.result} to be a string, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.result, input[1:-1])
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.bool:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                bool,
                                f"Expected inner value: {safe_nix_value.result} to be a bool, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.null:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                type(None),
                                f"Expected inner value: {safe_nix_value.result} to be a None, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.result, None)
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.path:
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
                        case nix.expr.Type.function:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                nix.expr.Function,
                                f"Expected inner value: {safe_nix_value.result} to be a Nix Function, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.external:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                nix.expr.ExternalValue,
                                f"Expected inner value: {safe_nix_value.result} to be a Nix ExternalValue, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                        case nix.expr.Type.attrs:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                Dict,
                                f"Expected inner value: {safe_nix_value.result} to be a Dict, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                            for k, v in (cast(Dict, safe_nix_value.result)).items():
                                self.assertIsInstance(k, str)
                                self.assertIsInstance(v, nix.expr.Value)
                        case nix.expr.Type.list:
                            self.assertIsInstance(
                                safe_nix_value.result,
                                List,
                                f"Expected inner value: {safe_nix_value.result} to be a List, got: {type(safe_nix_value.result)}",
                            )
                            self.assertEqual(safe_nix_value.error, None)
                            for v in cast(List, safe_nix_value.result):
                                self.assertIsInstance(v, nix.expr.Value)
                        case _:
                            assert_never()


# def test_eval_string(self):
#     v = safe_nix_eval('"a"')
#     self.assertEqual(v.type, nix.expr.Type.string)
#     self.assertEqual(v.success, True)
#     self.assertEqual(v.error, None)
#     self.assertEqual(v.result, "a")

# def test_eval_int(self):
#     v = safe_nix_eval("2")
#     self.assertEqual(v.type, nix.expr.Type.int)
#     self.assertEqual(v.success, True)
#     self.assertEqual(v.error, None)
#     self.assertEqual(v.result, 2)

# def test_eval_float(self):
#     v = safe_nix_eval("2.1")
#     self.assertEqual(v.type, nix.expr.Type.float)
#     self.assertEqual(v.success, True)
#     self.assertEqual(v.error, None)
#     self.assertEqual(v.result, 2.1)

# def test_eval_null(self):
#     v = safe_nix_eval("null")
#     self.assertEqual(v.type, nix.expr.Type.null)
#     self.assertEqual(v.success, True)
#     self.assertEqual(v.error, None)
#     self.assertEqual(v.result, None)

# def test_eval_path(self):
#     v = safe_nix_eval("./.")
#     self.assertEqual(v.type, nix.expr.Type.path)
#     self.assertEqual(v.success, True)
#     self.assertEqual(v.error, None)
#     print(v.result)
#     p = PurePath(os.path.join(os.path.dirname(__file__), "./"))
#     print(p)
#     self.assertEqual(v.result, p)

# def test_evaluates_integer(self):
#     (result, exception, success) = safe_nix_value_force(nix.eval("2"))
#     self.assertIsNone(exception, "expected exception to be none")
#     self.assertTrue(success, "expected success to be true")
#     self.assertEqual(result, 2, "expected result to be correct integer")

# def test_evaluates_float(self):
#     (result, exception, success) = safe_nix_value_force(nix.eval("2.1"))
#     self.assertIsNone(exception, "expected exception to be none")
#     self.assertTrue(success, "expected success to be true")
#     # self.assertEqual(result, 2.1, "expect result to be correct float")

# def test_evaluates_attrset(self):
#     (result, exception, success) = safe_nix_value_force(nix.eval("{ a = 2; }"))
#     self.assertIsNone(exception, "expected exception to be none")
#     self.assertTrue(success, "expected success to be true")
#     self.assertIsInstance(result, dict, "expect result to be instance of attrset")

#     result_keys = cast(Dict, result).keys()
#     print(result_keys)


if __name__ == "__main__":
    unittest.main()
