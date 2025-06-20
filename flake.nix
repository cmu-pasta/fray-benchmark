{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    uv2nix.url = "github:adisbladis/uv2nix";
    flake-utils.url = "github:numtide/flake-utils";
  };
  
  outputs = { self, nixpkgs, uv2nix, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Create the workspace from pyproject.toml
        workspace = uv2nix.lib.${system}.workspace.loadWorkspace { workspaceRoot = ./.; };
        
        # Create overlay
        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel"; # or "sdist"
        };
        
        # Create python with overlay
        python = pkgs.python311.override {
          packageOverrides = overlay;
        };
        
        # Get the package
        app = python.pkgs.fray-benchmark;
      in
      {
        packages.default = app;
        
        devShells.default = (pkgs.buildFHSEnv {
          name = "dev-shell";
          targetPkgs = pkgs: with pkgs; [
            python
            uv
            jdk21
            jdk11  # Added since you reference it in shellHook
            maven
            time
            cmake
            capnproto
            makeWrapper
            pkg-config
            which
            bash
            gdb
            libpfm
            procps
            zlib
            zstd
            # python311Packages.pexpect  # Removed - will use from virtual environment
          ];
          runScript = "bash";
          profile = ''
            export JDK11_HOME="${pkgs.jdk11.home}"
            export JDK21_HOME="${pkgs.jdk21.home}"
            
            # Create virtual environment with uv if it doesn't exist
            if [ ! -d ".venv" ]; then
              echo "Creating virtual environment with uv..."
              uv venv .venv
              echo "Installing dependencies with uv..."
              uv sync
            fi
            
            # Activate the virtual environment
            if [ -d ".venv/bin" ]; then
              export PATH="$PWD/.venv/bin:$PATH"
              export VIRTUAL_ENV="$PWD/.venv"
              echo "Virtual environment activated: $VIRTUAL_ENV"
            fi
          '';
        }).env;
      });
}