{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
    flake-utils.url = "github:numtide/flake-utils";
  };
  
  outputs = { self, nixpkgs, poetry2nix, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs; }) mkPoetryApplication mkPoetryEnv;
      in
      {
        packages.default = mkPoetryApplication { projectDir = self; };
        
        devShells.default = (pkgs.buildFHSEnv {
          name = "dev-shell";
          targetPkgs = pkgs: with pkgs; [
            (mkPoetryEnv { projectDir = self; })
            poetry
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