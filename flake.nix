{
  description = "Flake for my static site generator";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs, ... }@inputs:
  let
    inherit (self) outputs;
    forAllSystems = nixpkgs.lib.genAttrs [
      "aarch64-linux"
      "i686-linux"
      "x86_64-linux"
      "aarch64-darwin"
      "x86_64-darwin"
    ];
  in
  rec {
    # custom packages and modification, exported as overlays
    overlays = import ./overlays { inherit inputs; };

    # custom packages
    # accessible through `nix build`, `nix shell`, etc
    packages = forAllSystems (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in import ./pkgs { inherit pkgs; }
    );

    # Devshell
    # Acessibe through `nix develop` or `nix-shell` (legacy)
    devShells = forAllSystems (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            self.overlays.additions
            self.overlays.modifications
            # self.overlays.unstable-packages
          ];
        };
      in {
        default = pkgs.mkShell ({
          # at compile time
          nativeBuildInputs = [
          ];

          # at run time
          buildInputs = with pkgs; [
            bootdev
            go
            python312
            python312Packages.ipython
            python312Packages.pynvim
            python312Packages.rich
            ruff
            ruff-lsp
            ward
            treefmt
          ];

          shellHook = ''
          # Append src directory to PYTHONPATH
          # for development
          export PYTHONPATH="$PYTHONPATH:$PWD/src"
          '';
        });
      }
    );
  };
}

# {
#   description = "Flake for my static site generator";
#   inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
#   inputs.flake-utils.url = "github:numtide/flake-utils";
#
#   outputs = { nixpkgs, flake-utils, ... }:
#     flake-utils.lib.eachDefaultSystem (system:
#       let
#         pkgs = nixpkgs.legacyPackages.${system};
#         my-python-packages = ps: with ps; [
#           ipython
#           pynvim
#           rich
#           ward
#         ];
#       in
#       {
#         devShells.default = pkgs.mkShell {
#           packages = with pkgs; [
#             (python312.withPackages my-python-packages)
#             ruff
#             treefmt
#           ];
#         };
#       });
# }
