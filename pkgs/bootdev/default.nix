{ lib
, buildGoModule
, fetchFromGitHub
}:

  buildGoModule rec {
    pname = "bootdev";
    version = "1.4.0";

    src = fetchFromGitHub {
      owner = "bootdotdev";
      repo = "bootdev";
      rev = "f1948554ef1c7127962846ed1249454a755fb54e";
      hash = "sha256-wjNFYQkwRFTEaEiLxZhEYu7wrgM8kZpxXi6bkNjNJ8w=";
    };

    vendorHash = "sha256-v5P+Pt9weZ6+kkxfgpk+8GIOJRqp+Jx5uF3AJdRnp0s=";

    meta = with lib; {
      description = "Official command line tool for Boot.dev";
      homepage = "https://github.com/bootdotdev/bootdev";
      license = licenses.mit;
      maintainers = with maintainers; [ yannip ];
      mainProgram = "bootdev";
    };

  }

