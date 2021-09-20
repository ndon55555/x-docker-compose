import argparse
import subprocess
import sys
import tempfile

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Any unspecified args are forwarded to docker-compose."
            " Run without any args to get the help text of docker-compose."
        )
    )
    parser.add_argument(
        "--net",
        type=str,
        required=False,
        help="name of a Docker network to run docker-compose inside of",
    )
    args, unknown_args = parser.parse_known_args()

    compose_override = {}
    if args.net:
        compose_override = {
            "networks": {"default": {"name": args.net}},
        }

    with tempfile.NamedTemporaryFile() as f:
        content = yaml.safe_dump(compose_override)
        f.write(content.encode())
        f.flush()

        # TODO What if the unknown args include --file args as well?
        compose_args = ["--file", "docker-compose.yml", "--file", f.name, *unknown_args]
        result = subprocess.run(["docker-compose", *compose_args])
        sys.exit(result.returncode)
