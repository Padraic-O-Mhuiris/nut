{
  description = "Description for the project";

  inputs = {
    # nixpkgs.url = "github:NixOS/nixpkgs/master";

    python-nix.url = "github:tweag/python-nix";

    nix-c-bindings.url = "github:tweag/nix/nix-c-bindings";
    nixpkgs.follows = "nix-c-bindings/nixpkgs";

    flake-parts.url = "github:hercules-ci/flake-parts";
    flake-parts.inputs.nixpkgs-lib.follows = "nixpkgs";

  };

  outputs = inputs@{ flake-parts, nixpkgs, python-nix, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ];
      systems = nixpkgs.lib.systems.flakeExposed;

      perSystem = { pkgs, self', inputs', ... }: {
        devShells.default = pkgs.mkShell (let
          nix-c-bindings-package = inputs'.nix-c-bindings.packages.default;
          python-nix-packages = inputs'.python-nix.packages.default;
        in {
          buildInputs = [ nix-c-bindings-package ] ++ (with pkgs;
            [
              (python3.withPackages
                (p: [ python-nix-packages ] ++ (with p; [ click ])))
            ]);
        });
      };

      flake = let
        inherit (nixpkgs) lib;

        nut = import ./nix { inherit lib; };

        inherit (nut) Test TestCase TestBlock Assertion;
        pkgs = inputs.nixpkgs.legacyPackages.x86_64-linux;
      in {
        inherit inputs;
        inherit lib;
        inherit nut;

        test = Test "MyTest" [ (TestCase "TestCase 0" (Assertion.equals 1 1)) ];
      };
    };
}
