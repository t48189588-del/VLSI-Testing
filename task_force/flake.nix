#
# Enable this shell by calling 'nix develop' in the same directory as this file.
#

{
  description = "project development shell";

  inputs = {
    # 'quaigh' (logic synthesis / ATPG) is not in nixpkgs. The nl2bench overlay
    # builds it from crates.io via naersk and pulls in nix-eda (and its nixpkgs).
    nl2bench.url = "github:donn/nl2bench";
  };

  outputs = { self, nl2bench }:
    let
      nix-eda = nl2bench.inputs.nix-eda;
      nixpkgs = nix-eda.inputs.nixpkgs;
    in {
      devShells = nix-eda.forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ nix-eda.overlays.default nl2bench.overlays.default ];
          };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.uv
              pkgs.quaigh
            ];
          };
        }
      );
    };
}
