{ lib }:

let

  inherit (lib.strings) substring;

  inherit (lib.lists) imap0 isList foldr foldl;

  testType = { EQUALS = "EQUALS"; };

  generateTestId = message: entropy:
    let
      idHash =
        substring 0 10 (builtins.hashString "sha256" "${entropy}:${message}");
    in "${entropy}::${idHash}";

in rec {
  treeMap = fn: testMatrix:
    foldl (acc: item:
      if (item.__test__ == "__test_branch__") then
        acc ++ [ (treeMap fn item) ]
      else
        acc ++ [ (fn item) ]) [ ] testMatrix.value;

  Assertion.equals = left: right: {
    type = testType.EQUALS;
    inherit left right;
    __test__ = "__assertion__";
  };

  # TestCase
  TestCase = message: assertionFunctor: cntr:
    let id = generateTestId message cntr;
    in {
      __test__ = "__test_case__";
      value = assertionFunctor;
      inherit id message;
    };

  TestBlock = message: testMatrix: cntr:
    let id = generateTestId message cntr;
    in {
      __test__ = "__test_branch__";
      inherit id message;
      value =
        imap0 (idx: fn: (fn "${toString cntr}-${toString idx}")) testMatrix;
    };

  Test = message: testMatrix:
    let testTree = (imap0 (idx: fn: fn "${toString idx}") testMatrix);
    in {
      __test__ = "__test_root__";
      inherit message;
      value = testTree;
    };
}
