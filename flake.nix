{
  description = "Description for the project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    devenv.url = "github:cachix/devenv";
    nix2container.url = "github:nlewo/nix2container";
    nix2container.inputs.nixpkgs.follows = "nixpkgs";
    mk-shell-bin.url = "github:rrbutani/nix-mk-shell-bin";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = [ "x86_64-linux" "i686-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        # Per-system attributes can be defined here. The self' and inputs'
        # module parameters provide easy access to attributes of the same
        # system.

        # Equivalent to  inputs'.nixpkgs.legacyPackages.hello;
        packages.default = pkgs.hello;

        devenv.shells.default = {
          name = "SWISS";

          languages.python = {
            enable = true;
            version = "3.11.3";
            venv.enable = true;
            venv.quiet = true;
            venv.requirements = ./requirements.txt;
          };

          services.postgres = {
            enable = true;
            # TODO: use secrets for username, password, team #, etc.
            initialScript = ''
              CREATE USER developer WITH PASSWORD 'DEVELOPER';
              INSERT INTO entry_team (id, number, name, colour, pick_status, glance) values(0000, 0000, 'DeveloperTech 0000', '#0', 0, '\');
              INSERT INTO entry_event values(0, 'default', 'default', 0, '2000-01-01', '2000-01-02', false, 'default');
              INSERT INTO entry_orgsettings (id, allow_photos, new_user_creation, new_user_position, current_event_id, team_id) values(0, true, 'AA', 'GS', 0, 0000);
              INSERT INTO entry_organization (id, name, reg_id, settings_id, team_id) values(0, 'DeveloperTech 0000', '4710e98a-e55a-4941-8963-5d6e12179f22', 0, 0000);
              INSERT INTO entry_orgmember (id, tutorial_completed, position, user_id, team_id) values(0, false, 'LS', 1, 0000);
            '';
            listen_addresses = "*";
          };

          imports = [
            # This is just like the imports in devenv.nix.
            # See https://devenv.sh/guides/using-with-flake-parts/#import-a-devenv-module
            # ./devenv-foo.nix
          ];

          # https://devenv.sh/reference/options/
          packages = with pkgs; [ config.packages.default 
            postgresql.lib postgresql
            nginx
            gcc
          ];

          enterShell = ''
            echo python manage.py makemigrations
            echo python manage.py migrate
            echo python manage.py createsuperuser
          '';
        };

      };
      flake = {
        # The usual flake attributes can be defined here, including system-
        # agnostic ones like nixosModule and system-enumerating ones, although
        # those are more easily expressed in perSystem.

      };
    };
}
