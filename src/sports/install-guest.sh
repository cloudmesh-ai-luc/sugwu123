#!/usr/bin/env bash
# Install SPORTSSTATS on an existing Ubuntu VM, without changing cmx.
set -euo pipefail

project_root=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
guest_user=$(id -un)
mode=install
if [ "$#" -gt 0 ]; then mode=$1; fi

render_unit() {
    cat <<UNIT
[Unit]
Description=SPORTSSTATS historical NBA dashboard
After=network.target

[Service]
User=$guest_user
WorkingDirectory=$project_root
ExecStart=/usr/bin/python3 -m sports --db sports/data/history.sqlite3 serve --host 127.0.0.1 --port 8765
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=3
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
UNIT
}

if [ "$mode" = --print-unit ]; then render_unit; exit 0; fi
if [ "$mode" != install ] || [ "$(uname -s)" != Linux ]; then
    printf '%s\n' 'Run this on the Ubuntu VM, or use --print-unit to review the service.'
    exit 2
fi
case "$guest_user" in ubuntu|cc) ;; *) printf '%s\n' 'Run as the Ubuntu VM user (ubuntu or cc), without sudo.'; exit 2 ;; esac
if [ "$project_root" != "$HOME/sports-project" ]; then
    printf '%s\n' 'Place the sports source directory inside ~/sports-project first.'
    exit 2
fi
cd -- "$project_root"
sudo -n true
/usr/bin/python3 -c 'import sqlite3, sys; assert sys.version_info >= (3, 12), "Ubuntu 24.04 / Python 3.12+ is required"'
/usr/bin/python3 -m unittest discover -s sports/tests -v
if [ ! -s sports/data/history.sqlite3 ]; then
    /usr/bin/python3 -m sports.history --season 2015
fi

# Port 8765 keeps the existing port-8000 presentation demo available.
render_unit | sudo -n tee /etc/systemd/system/sportsstats.service >/dev/null
sudo -n systemctl daemon-reload
sudo -n systemctl enable sportsstats.service
sudo -n systemctl restart sportsstats.service

/usr/bin/python3 - <<'PY'
import json
import math
import socket
import subprocess
import time
import urllib.error
import urllib.request

base = "http://127.0.0.1:8765"
for attempt in range(15):
    try:
        with urllib.request.urlopen(base + "/api/health", timeout=2) as response:
            health = json.load(response)
        if health.get("status") == "ok":
            break
    except (OSError, urllib.error.URLError):
        pass
    time.sleep(1)
else:
    raise SystemExit("SPORTSSTATS did not become healthy; inspect journalctl -u sportsstats")

subprocess.run(["systemctl", "is-active", "--quiet", "sportsstats.service"], check=True)
assert health["dataset"]["kind"] == "imported", "Expected the historical dataset"
assert health["dataset"]["rows"] == 2460, "Expected 2,460 team-game rows"
with urllib.request.urlopen(base + "/api/model?team=CHI&threshold=100.5", timeout=10) as response:
    result = json.load(response)
model = result["model"]
assert model["evaluated_games"] == 72, "Expected 72 evaluated Chicago games"
assert math.isclose(model["logistic_brier_score"], 0.2533129305645343, abs_tol=1e-9)
assert model["constant_half_brier_score"] == 0.25
print(json.dumps({
    "sportsstats": "healthy", "host": socket.gethostname(), "port": 8765,
    "rows": health["dataset"]["rows"], "evaluated_games": model["evaluated_games"],
    "logistic_brier": model["logistic_brier_score"],
    "constant_half_brier": model["constant_half_brier_score"]
}, indent=2))
PY
