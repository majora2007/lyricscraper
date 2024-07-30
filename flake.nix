{
  description = "lyricscraper";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/b73c2221a46c13557b1b3be9c2070cc42cf01eb3";
    flake-utils.url = "github:numtide/flake-utils";
    libs.url = "github:lomenzel/python-modules";
  };

  outputs =
    {
      self,
      nixpkgs,
      libs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        pylibs = libs.packages.${system};
        python = pkgs.python311.withPackages (
          ps: with ps; [
            pylibs.gooey
            mutagen
            requests
            beautifulsoup4
            selenium
          ]
        );
      in
      {
        devShell = pkgs.mkShell { nativeBuildInputs = [ python ]; };
        packages = rec {
          default = lyricscraper;
          lyricscraper = pkgs.writeShellScriptBin "lyricscraper" ''
            ${python}/bin/python ${./.}/main.py
          '';
        };
      }

    );

}
