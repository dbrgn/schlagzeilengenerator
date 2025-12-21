{
  description = "Schlagzeilengenerator - A tabloid press headline generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        packages.default = pkgs.callPackage ./package.nix {};

        # Alias for convenience
        packages.schlagzeilengenerator = self.packages.${system}.default;
      }
    )
    // {
      # NixOS module (not system-specific)
      nixosModules.default = import ./module.nix;

      # Alias for convenience
      nixosModules.schlagzeilengenerator = self.nixosModules.default;

      # Overlay for adding the package to pkgs
      overlays.default = final: prev: {
        schlagzeilengenerator = final.callPackage ./package.nix {};
      };
    };
}
