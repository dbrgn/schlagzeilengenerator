{
  lib,
  python3,
  python3Packages,
}:
python3Packages.buildPythonApplication rec {
  pname = "schlagzeilengenerator";
  version = "1.0.0";
  format = "pyproject";

  src = lib.cleanSourceWith {
    src = ../.;
    filter = path: type: let
      baseName = baseNameOf path;
      relPath = lib.removePrefix "${toString ../.}/" path;
    in
      # Include app/ directory and its contents
      lib.hasPrefix "app/" relPath
      ||
      # Include specific root files
      builtins.elem baseName ["README.md" "LICENSE"];
  };

  # Point to the app subdirectory for Python package
  sourceRoot = "source/app";

  nativeBuildInputs = with python3Packages; [
    setuptools
  ];

  propagatedBuildInputs = with python3Packages; [
    flask
    gunicorn
  ];

  # Don't run tests (there are none)
  doCheck = false;

  # Install additional data files
  postInstall = ''
        # Copy data files
        mkdir -p $out/share/schlagzeilengenerator
        cp -r data $out/share/schlagzeilengenerator/
        cp -r static $out/share/schlagzeilengenerator/
        cp -r templates $out/share/schlagzeilengenerator/

        # Create wrapper script
        mkdir -p $out/bin
        cat > $out/bin/schlagzeilengenerator <<EOF
    #!/bin/sh
    cd $out/share/schlagzeilengenerator
    export PYTHONPATH="$out/${python3.sitePackages}:\$PYTHONPATH"
    exec ${python3Packages.gunicorn}/bin/gunicorn \\
      --bind "\''${SCHLAGZEILEN_HOST:-127.0.0.1}:\''${SCHLAGZEILEN_PORT:-8000}" \\
      --workers 2 \\
      --threads 2 \\
      --access-logfile - \\
      --error-logfile - \\
      app:app "\$@"
    EOF
        chmod +x $out/bin/schlagzeilengenerator
  '';

  meta = with lib; {
    description = "A small web application to generate tabloid press headlines";
    homepage = "https://schlagzeilengenerator.ch";
    license = licenses.bsd3;
    maintainers = [];
    mainProgram = "schlagzeilengenerator";
  };
}
