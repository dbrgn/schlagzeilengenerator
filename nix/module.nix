{
  config,
  lib,
  pkgs,
  ...
}: let
  cfg = config.services.schlagzeilengenerator;
in {
  options.services.schlagzeilengenerator = {
    enable = lib.mkEnableOption "Schlagzeilengenerator tabloid headline generator";

    domain = lib.mkOption {
      type = lib.types.nullOr lib.types.str;
      default = null;
      example = "schlagzeilengenerator.ch";
      description = "Domain name for the application";
    };

    port = lib.mkOption {
      type = lib.types.port;
      default = 8000;
      description = "Internal port for Gunicorn to bind to";
    };

    host = lib.mkOption {
      type = lib.types.str;
      default = "127.0.0.1";
      description = "Host address for Gunicorn to bind to";
    };

    nginx = {
      enable = lib.mkOption {
        type = lib.types.bool;
        default = false;
        description = "Enable nginx virtual host configuration";
      };

      forceSSL = lib.mkOption {
        type = lib.types.bool;
        default = true;
        description = "Force SSL/TLS for all connections";
      };

      enableACME = lib.mkOption {
        type = lib.types.bool;
        default = true;
        description = "Enable ACME (Let's Encrypt) for automatic SSL certificates for this domain";
      };

      useACMEHost = lib.mkOption {
        type = lib.types.nullOr lib.types.str;
        default = null;
        example = "example.com";
        description = "Use an existing ACME certificate from another host (e.g., for wildcard certificates). Takes precedence over enableACME.";
      };

      extraConfig = lib.mkOption {
        type = lib.types.lines;
        default = "";
        description = "Extra nginx configuration for the virtual host";
      };
    };
  };

  config = lib.mkIf cfg.enable {
    assertions = [
      {
        assertion = cfg.nginx.enable -> cfg.domain != null;
        message = "services.schlagzeilengenerator.domain must be set when nginx is enabled";
      }
      {
        assertion = cfg.nginx.enableACME -> cfg.nginx.forceSSL;
        message = "services.schlagzeilengenerator.nginx.forceSSL must be true when enableACME is true";
      }
      {
        assertion = cfg.nginx.useACMEHost != null -> cfg.nginx.forceSSL;
        message = "services.schlagzeilengenerator.nginx.forceSSL must be true when useACMEHost is set";
      }
      {
        assertion = (cfg.nginx.enableACME && cfg.nginx.useACMEHost != null) -> false;
        message = "services.schlagzeilengenerator.nginx: cannot use both enableACME and useACMEHost";
      }
    ];

    systemd.services.schlagzeilengenerator = {
      description = "Schlagzeilengenerator tabloid headline generator";
      after = ["network.target"];
      wantedBy = ["multi-user.target"];

      environment = {
        SCHLAGZEILEN_HOST = cfg.host;
        SCHLAGZEILEN_PORT = toString cfg.port;
        APP_URL =
          if cfg.domain != null
          then "https://${cfg.domain}/"
          else "http://${cfg.host}:${toString cfg.port}/";
      };

      serviceConfig = {
        Type = "notify";
        DynamicUser = true;
        ExecStart = "${pkgs.schlagzeilengenerator}/bin/schlagzeilengenerator";
        Restart = "on-failure";
        RestartSec = "5s";

        # Security hardening. (Note: DynamicUser already implies PrivateTmp, RemoveIPC,
        # ProtectSystem=strict, ProtectHome=read-only, NoNewPrivileges.)
        PrivateDevices = true;
        ProtectKernelTunables = true;
        ProtectKernelModules = true;
        ProtectControlGroups = true;
        ProtectClock = true;
        ProtectHostname = true;
        ProtectProc = "invisible";
        ProcSubset = "pid";
        RestrictAddressFamilies = ["AF_UNIX" "AF_INET" "AF_INET6"];
        RestrictNamespaces = true;
        LockPersonality = true;
        RestrictRealtime = true;
        RestrictSUIDSGID = true;
        SystemCallFilter = ["@system-service" "~@privileged"];
        CapabilityBoundingSet = "";
        UMask = "0077";
      };
    };

    services.nginx = lib.mkIf cfg.nginx.enable {
      enable = true;
      virtualHosts.${cfg.domain} = {
        forceSSL = cfg.nginx.forceSSL;
        enableACME = cfg.nginx.useACMEHost == null && cfg.nginx.enableACME;
        useACMEHost = cfg.nginx.useACMEHost;

        locations."/" = {
          proxyPass = "http://${cfg.host}:${toString cfg.port}";
          proxyWebsockets = true;
          extraConfig = ''
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
          '';
        };

        locations."/static/" = {
          alias = "${pkgs.schlagzeilengenerator}/share/schlagzeilengenerator/static/";
          extraConfig = ''
            expires 30d;
            add_header Cache-Control "public, immutable";
          '';
        };

        extraConfig = cfg.nginx.extraConfig;
      };
    };
  };
}
