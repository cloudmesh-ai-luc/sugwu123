# SPORTSSTATS on an Existing Ubuntu VM

This installs the same historical NBA application on an existing Ubuntu 24.04 guest. It changes only the student's application and a new `sportsstats.service`; it does not edit cmx, launch a VM, or stop the working port-8000 dashboard. It is prepared and locally checked, not yet verified on a live guest.

## Review and Package

Review `sports/install-guest.sh` before running it. The guest must use the account `ubuntu` or `cc`, with non-interactive sudo. Python 3.12+ and SQLite support are required. The source belongs in `~/sports-project`.

After reviewing and committing the installer in the student's course repository, make a source-only archive on the Mac:

```bash
git archive --format=tar.gz --output=/tmp/SPORTSSTATS-source.tar.gz HEAD sports
```

The archive uses committed source. Raw data and keys are excluded. Existing databases are not replaced by this installer.

## Multipass

First check `multipass list`. These commands target the existing project VM `sports-midterm`; use them only if that VM is present and running.

```bash
multipass transfer /tmp/SPORTSSTATS-source.tar.gz sports-midterm:/home/ubuntu/SPORTSSTATS-source.tar.gz
multipass exec sports-midterm -- bash -lc 'mkdir -p ~/sports-project && tar -xzf ~/SPORTSSTATS-source.tar.gz -C ~/sports-project && bash ~/sports-project/sports/install-guest.sh'
```

## AWS or Chameleon

Use the actual guest address, key, and username from the existing VM. AWS Ubuntu uses `ubuntu`; the earlier Chameleon image used `cc`. The example placeholders below must be replaced with those values. Keep private key contents on the Mac.

```bash
scp -i KEY_PATH /tmp/SPORTSSTATS-source.tar.gz GUEST_USER@GUEST_ADDRESS:SPORTSSTATS-source.tar.gz
ssh -i KEY_PATH -o ServerAliveInterval=30 GUEST_USER@GUEST_ADDRESS 'mkdir -p ~/sports-project && tar -xzf ~/SPORTSSTATS-source.tar.gz -C ~/sports-project && bash ~/sports-project/sports/install-guest.sh'
```

The installer runs the application tests, imports the pinned historical dataset if missing, and enables a systemd service. It then checks the real HTTP health and model output. Expected output includes 2,460 rows, 72 evaluated Chicago games, logistic Brier 0.2533129305645343, and constant Brier 0.25. Save actual output for each guest; a prepared command is not a live result.

## View the Separate Service

The service binds to guest `127.0.0.1:8765`. To view a remote SSH guest from the Mac, open another Terminal tab with a distinct unused local port:

```bash
ssh -i KEY_PATH -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -N -L 127.0.0.1:8002:127.0.0.1:8765 GUEST_USER@GUEST_ADDRESS
```

Open <http://127.0.0.1:8002> and keep that tunnel tab open. Use a different local port for another guest. Do not replace the existing AWS port-8001 tunnel until the new service has been verified. A Multipass guest can also be checked with `multipass exec sports-midterm -- curl -fsS http://127.0.0.1:8765/api/health`.

For a failed install, inspect the guest's `systemctl status sportsstats.service` and `journalctl -u sportsstats.service --no-pager -n 40`. A successful install does not establish VM provisioning through cmx or complete the instructor's three-cloud requirement. Those results must be checked separately.

Acknowledgment: OpenAI Codex wrote this installer and guide. Live guest installation and student review are still needed.
