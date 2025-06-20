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
            python3Packages.gitpython
            jdk21
            jdk11  # Added since you reference it in shellHook
            maven
            time
            cmake
            capnproto
            makeWrapper
            pkg-config
            python3
            which
            bash
            gdb
            libpfm
            procps
            zlib
            zstd
            python312Packages.pexpect
          ];
          runScript = "bash";
          profile = ''
            export JDK11_HOME="${pkgs.jdk11.home}"
            export JDK21_HOME="${pkgs.jdk21.home}"
          '';
        }).env;
      });
}