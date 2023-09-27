{
  description = "Description for the project";

  inputs = { inputs.nixpkgs.url = "github:NixOS/nixpkgs/master"; };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ];
      systems = inputs.nixpkgs.lib.systems.flakeExposed;
      # perSystem = { config, self', inputs', pkgs, system, ... }:
      #   {
      #   };
      flake = let
        lib = inputs.nixpkgs.lib;
        nut = import ./nix { inherit lib; };
        inherit (nut) Test TestCase TestBlock Assertion;
      in {
        inherit lib;

        inherit nut;

        test = Test "MyTest" [
          (TestCase "TestCase 0" (Assertion.equals testExpr { a = 3; }))
          (TestBlock "TestCase 1" (let inherit (testExpr) y;
          in [
            (TestCase "TestCase 1-0" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-1" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-2" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-3" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-4" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-5" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-6" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-7" (Assertion.equals y { a = 3; }))
            (TestCase "TestCase 1-8" (Assertion.equals y { a = 3; }))
          ]))
        ];
      };
    };
}
