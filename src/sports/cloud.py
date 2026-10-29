"""Plan three-cloud operations or smoke-test an already deployed sports VM."""

import argparse
import json
import re
import shlex
import subprocess

from .vm import validate_name


ROLES = {"multipass": "Local development and repeatable demo",
         "chameleon": "OpenStack deployment and cross-cloud reproduction at KVM@TACC",
         "aws": "Short CPU model-evaluation run on Amazon EC2",
         "google": "Short CPU model-evaluation run on Google Compute Engine"}
NAMES = {"multipass": "sports-midterm", "chameleon": "sports-chameleon",
         "aws": "SPORTSSTATS", "google": "sports-google"}


def validate_cloud_name(cloud, name):
    # An EC2 Name tag can use the project title. Local VM safeguards stay intact.
    if cloud == "aws" and name == "SPORTSSTATS":
        return name
    return validate_name(name)


def plan(cloud, name):
    validate_cloud_name(cloud, name)
    base = ["cmx", "vm", "--cloud", cloud]
    return {"cloud": cloud, "role": ROLES[cloud], "vm": name,
            "create": base + ["start", name], "inventory": base + ["list"],
            "information": base + ["info", name],
            "guest_execution": base + ["run", name, "python3 --version"],
            "status": "Plan only. Credentials, quotas, SSH keys and live results are not verified."}


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text):
    """Strip ANSI escape sequences from CLI output."""
    return ANSI_ESCAPE_RE.sub("", text or "")


def smoke_payload(output):
    # Rich may add a provider banner. A zero CLI exit alone does not prove success.
    plain = strip_ansi(output)
    for match in re.finditer(r"\{", plain):
        try:
            result, _ = json.JSONDecoder().raw_decode(plain[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(result, dict) and result.get("sports_smoke") == "ok":
            if result.get("rows", 0) > 0 and result.get("evaluated_games", 0) > 0:
                return result
    raise ValueError("Guest did not return a validated sports-analysis result")


def smoke(cloud, name, team, threshold):
    validate_cloud_name(cloud, name)
    code = ("import json; from sports.store import Store; from sports.model import analyze_model; "
            f"r=analyze_model(Store('sports/data/history.sqlite3'),{team!r},threshold={threshold!r}); "
            "print(json.dumps(dict(sports_smoke='ok',rows=r['dataset']['rows'],"
            "evaluated_games=r['model']['evaluated_games'],"
            "logistic_brier_score=r['model']['logistic_brier_score']),indent=2))")
    guest = "cd ~/sports-project && python3 -c " + shlex.quote(code)
    command = ["cmx", "vm", "--cloud", cloud, "run", name, guest]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)
    return {"cloud": cloud, "vm": name, "command": command,
            "result": smoke_payload(result.stdout), "execution": "live cmx guest command"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "smoke"])
    parser.add_argument("--cloud", choices=sorted(ROLES), required=True)
    parser.add_argument("--name")
    parser.add_argument("--team", default="CHI")
    parser.add_argument("--threshold", type=float, default=100.5)
    args = parser.parse_args(argv)
    try:
        name = args.name or NAMES[args.cloud]
        result = plan(args.cloud, name) if args.action == "plan" else smoke(args.cloud, name, args.team, args.threshold)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
