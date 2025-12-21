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

        # Formatter for `nix fmt`
        formatter = pkgs.alejandra;

        # Checks run by `nix flake check`
        checks = {
          # Verify the package builds
          package = self.packages.${system}.default;

          # Evaluate the NixOS module to catch configuration errors
          module =
            (nixpkgs.lib.nixosSystem {
              inherit system;
              modules = [
                self.nixosModules.default
                {
                  # Minimal config to evaluate the module
                  security.acme = {
                    defaults.email = "example@example.com";
                    acceptTerms = true;
                  };
                  services.schlagzeilengenerator = {
                    enable = true;
                    domain = "example.com";
                    nginx.enable = true;
                  };

                  # Required stub options for evaluation
                  nixpkgs.hostPlatform = system;
                  boot.loader.grub.enable = false;
                  fileSystems."/".device = "nodev";
                  system.stateVersion = "25.11";
                }
              ];
            })
            .config
            .system
            .build
            .toplevel;
        };
      }
    )
    // {
      # NixOS module (not system-specific)
      # Includes the overlay so pkgs.schlagzeilengenerator is available
      nixosModules.default = {
        imports = [./module.nix];
        nixpkgs.overlays = [self.overlays.default];
      };

      # Overlay for adding the package to pkgs
      overlays.default = final: prev: {
        schlagzeilengenerator = final.callPackage ./package.nix {};
      };
    };
}
