"""Automate a dedicated local Multipass VM without touching coursework VMs."""

import argparse
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path


BOOTSTRAP = """set -eu
mkdir -p /home/ubuntu/sports-project
tar -xzf /home/ubuntu/sports-source.tar.gz -C /home/ubuntu/sports-project
cd /home/ubuntu/sports-project
if ! python3 -c 'import sqlite3, unittest' 2>/dev/null; then
    sudo apt-get update
    sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y python3
fi
python3 -c 'import sqlite3, sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"'
python3 -m unittest discover -s sports/tests -v
if [ ! -s sports/data/sports.sqlite3 ]; then
    python3 -m sports demo
fi
sudo tee /etc/systemd/system/sports-midterm.service >/dev/null <<'UNIT'
[Unit]
Description=Sports statistics prototype
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/sports-project
ExecStart=/usr/bin/python3 -m sports serve --host 0.0.0.0 --port 8000
Environment=PYTHONUNBUFFERED=1
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable sports-midterm.service
sudo systemctl restart sports-midterm.service
python3 - <<'PY'
import json, time, urllib.error, urllib.request
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=2) as response:
            result = json.load(response)
        assert result['status'] == 'ok'
        print(json.dumps(result))
        break
    except (OSError, urllib.error.URLError):
        time.sleep(1)
else:
    raise SystemExit('Sports service did not become healthy')
PY
"""


def validate_name(name):
    if len(name) > 45 or not re.fullmatch(r"sports-[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Use a dedicated VM name beginning with sports- (letters, digits, hyphens)")
    return name


def run(*arguments, capture=False, input_text=None):
    return subprocess.run(["multipass", *arguments], check=True, text=True,
                          capture_output=capture, input=input_text)


def archive_source(target, root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parent
    with tarfile.open(target, "w:gz") as archive:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if path.is_symlink() or "data" in relative.parts or "__pycache__" in relative.parts:
                continue
            if path.is_file() and (path.suffix in {".py", ".html", ".js", ".css", ".md"}
                                   or path.name == "Makefile"):
                archive.add(path, arcname=str(Path("sports") / relative))


def deploy(name):
    inventory = json.loads(run("list", "--format", "json", capture=True).stdout)
    instance = next((item for item in inventory["list"] if item["name"] == name), None)
    if instance is None:
        run("launch", "24.04", "--name", name, "--cpus", "2", "--memory", "2G", "--disk", "10G")
    elif instance["state"] == "Deleted":
        raise ValueError("This project VM is deleted. Recover it or choose another sports- name.")
    elif instance["state"] != "Running":
        run("start", name)
    with tempfile.TemporaryDirectory() as temporary:
        archive = Path(temporary) / "sports-source.tar.gz"
        archive_source(archive)
        run("transfer", str(archive), f"{name}:/home/ubuntu/sports-source.tar.gz")
        run("exec", name, "--", "bash", "-s", input_text=BOOTSTRAP)
    show_status(name)


def show_status(name):
    result = json.loads(run("info", name, "--format", "json", capture=True).stdout)
    print(json.dumps(result, indent=2))
    for address in result["info"][name].get("ipv4", []):
        if address:
            print(f"Dashboard: http://{address}:8000")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Manage only a dedicated sports project VM")
    parser.add_argument("action", choices=["deploy", "status", "start", "stop", "delete"])
    parser.add_argument("--name", default="sports-midterm")
    parser.add_argument("--confirm-name", help="Required for deletion; must equal --name")
    arguments = parser.parse_args(argv)
    try:
        name = validate_name(arguments.name)
        if arguments.action == "delete" and arguments.confirm_name != name:
            raise ValueError("Deletion requires --confirm-name matching the dedicated project VM name")
        if not shutil.which("multipass"):
            raise ValueError("Multipass is required on the host computer")
        if arguments.action == "deploy":
            deploy(name)
        elif arguments.action == "status":
            show_status(name)
        elif arguments.action == "delete":
            run("delete", "--purge", name)
        else:
            run(arguments.action, name)
            show_status(name)
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
