{
  description = "Flake for my static site generator";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        my-python-packages = ps: with ps; [
          ipython
          pynvim
          rich
          ward
        ];
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            (python312.withPackages my-python-packages)
            ruff
            treefmt
          ];
        };
      });
}
