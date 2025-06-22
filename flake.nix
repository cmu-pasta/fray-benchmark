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
        workspace = uv2nix.lib.${system}.workspace.loadWorkspace { workspaceRoot = ./.; };
        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel"; # or "sdist"
        };
        python = pkgs.python311.override {
          packageOverrides = overlay;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python
            uv
            jdk21
            jdk11
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
            zlib.dev
            zstd.dev
            gcc
            vim
          ];
          
          shellHook = ''
            export JDK11_HOME="${pkgs.jdk11.home}"
            export JDK21_HOME="${pkgs.jdk21.home}"
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
            
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
              source .venv/bin/activate
              echo "Virtual environment activated: $VIRTUAL_ENV"
            fi
          '';
        };
      });
}