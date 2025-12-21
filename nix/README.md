# Nix Flake for Schlagzeilengenerator

This directory contains Nix packaging for the Schlagzeilengenerator application.

## Structure

- `flake.nix` - Main flake definition with inputs and outputs
- `package.nix` - Python package derivation (builds the app with Gunicorn)
- `module.nix` - NixOS module for systemd service and optional nginx integration

## Usage

### Building the Package

```bash
# From the repository root
nix build ./nix
```

### Using in NixOS Configuration

Add to your `flake.nix`:

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    schlagzeilengenerator.url = "github:dbrgn/schlagzeilengenerator?dir=nix";
  };

  outputs = { self, nixpkgs, schlagzeilengenerator }: {
    nixosConfigurations.myserver = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        schlagzeilengenerator.nixosModules.default
        {
          services.schlagzeilengenerator = {
            enable = true;
            domain = "schlagzeilengenerator.ch";
            nginx.enable = true;
          };
        }
      ];
    };
  };
}
```

### Configuration Options

#### Basic Options

- `services.schlagzeilengenerator.enable` - Enable the service (default: `false`)
- `services.schlagzeilengenerator.domain` - Domain name (required if nginx is enabled)
- `services.schlagzeilengenerator.port` - Internal port for Gunicorn (default: `8000`)
- `services.schlagzeilengenerator.host` - Bind address (default: `"127.0.0.1"`)
- `services.schlagzeilengenerator.user` - Service user (default: `"schlagzeilen"`)
- `services.schlagzeilengenerator.group` - Service group (default: `"schlagzeilen"`)

#### Nginx Options

- `services.schlagzeilengenerator.nginx.enable` - Enable nginx reverse proxy (default: `false`)
- `services.schlagzeilengenerator.nginx.forceSSL` - Force HTTPS (default: `true`)
- `services.schlagzeilengenerator.nginx.enableACME` - Request Let's Encrypt cert for this domain (default: `true`)
- `services.schlagzeilengenerator.nginx.useACMEHost` - Use existing cert from another ACME host (default: `null`, example: `"example.com"` for wildcard certs)
- `services.schlagzeilengenerator.nginx.extraConfig` - Additional nginx configuration

### Example Configurations

#### Minimal (without nginx)

```nix
services.schlagzeilengenerator = {
  enable = true;
  port = 8080;
};
```

#### Production with nginx and TLS

```nix
services.schlagzeilengenerator = {
  enable = true;
  domain = "headlines.example.com";
  
  nginx = {
    enable = true;
    forceSSL = true;
    enableACME = true;
  };
};

# Don't forget to configure ACME email
security.acme.defaults.email = "admin@example.com";
```

#### With existing certificate

```nix
# Assuming you have a wildcard cert configured for *.example.com
services.schlagzeilengenerator = {
  enable = true;
  domain = "headlines.example.com";

  nginx = {
    enable = true;
    useACMEHost = "example.com";  # Use the wildcard cert
  };
};
```

#### Without TLS

```nix
services.schlagzeilengenerator = {
  enable = true;
  domain = "dev.example.com";
  
  nginx = {
    enable = true;
    forceSSL = false;
    enableACME = false;
  };
};
```

## Testing Locally

You can test the package build without NixOS:

```bash
# From repository root
nix build ./nix

# Or from within nix/ directory
cd nix
nix build

# Run directly
./result/bin/schlagzeilengenerator

# The application will be available at http://127.0.0.1:8000
```

## Overlay

The flake also provides an overlay for adding the package to your nixpkgs:

```nix
nixpkgs.overlays = [ schlagzeilengenerator.overlays.default ];

# Now you can use pkgs.schlagzeilengenerator anywhere
```

## Development

To make changes to the Nix packaging:

1. Edit the relevant file (`package.nix`, `module.nix`, or `flake.nix`)
2. Test with `nix flake check`
3. Build with `nix build`
4. Test the NixOS module in a VM or container

## Security

The systemd service includes hardening options:

- Runs as unprivileged user
- Private /tmp
- Restricted system calls
- No new privileges
- Protected kernel interfaces
- Network-only access

## License

Same as the main application (BSD-3-Clause).
