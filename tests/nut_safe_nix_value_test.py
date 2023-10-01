from pathlib import PurePath
import unittest
import nix.expr
import os
import pytest
from allpairspy import AllPairs
from nut.nut_safe_nix_value import safe_nix_eval


class Test__nut_safe_nix_value(unittest.TestCase):
    @pytest.mark.parametrize(
        [
            "input_value",
        ],
        [
            values
            for values in AllPairs(
                [
                    [
                        '"a"',
                        '"wlxqnxnqkwkqkw"',
                        "2",
                        "2.11212",
                        "null",
                    ],
                ]
            )
        ],
    )
    def test__safe_nix_eval(self, input_value):
        parameters = [
            ["BrandX", "BrandY"],
            ["Small", "Medium", "Large"],
            ["Red", "Green", "Blue"],
        ]
        for test_case in AllPairs(parameters):
            with self.subTest(test_case=test_case):
                brand, size, color = test_case
                # Perform the actual test with the generated test_case
                self.run(brand, size, color)

    def run(self, brand, size, color):
        print(brand, size, color)
        # if brand == "BrandX":
        #     self.assertNotEqual(
        #         color, "Red", f"BrandX should not have color Red. Size: {size}"
        #     )

        # # Assert that if size is "Small", brand should not be "BrandY"
        # if size == "Small":
        #     self.assertNotEqual(
        #         brand,
        #         "BrandY",
        #         f"Small size should not have brand BrandY. Color: {color}",
        #     )


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
