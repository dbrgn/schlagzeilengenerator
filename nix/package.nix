{
  stdenv,
  lib,
  python3,
  makeWrapper,
}: let
  python = python3.withPackages (packages: [
    packages.flask
    packages.gunicorn
  ]);
in
  stdenv.mkDerivation {
    pname = "schlagzeilengenerator";
    version = "1.0.0";

    src = ../app;

    nativeBuildInputs = [makeWrapper];

    installPhase = ''
      runHook preInstall

      # Copy application files
      mkdir -p $out/share/schlagzeilengenerator
      cp -r . $out/share/schlagzeilengenerator/

      # Create wrapper script
      mkdir -p $out/bin
      makeWrapper ${python}/bin/gunicorn $out/bin/schlagzeilengenerator \
        --chdir $out/share/schlagzeilengenerator \
        --add-flags "--bind \"\''${SCHLAGZEILEN_HOST:-127.0.0.1}:\''${SCHLAGZEILEN_PORT:-8000}\"" \
        --add-flags "--workers 2" \
        --add-flags "--threads 2" \
        --add-flags "--access-logfile -" \
        --add-flags "--error-logfile -" \
        --add-flags "app:app"

      runHook postInstall
    '';

    meta = with lib; {
      description = "A small web application to generate tabloid press headlines";
      homepage = "https://schlagzeilengenerator.ch";
      license = licenses.bsd3;
      maintainers = [];
      mainProgram = "schlagzeilengenerator";
    };
  }
