# SPORTSSTATS: AWS Setup

AWS is the selected public cloud. On October 15, the student connected to the running EC2 instance, transferred the source, passed all 34 application tests, ran the historical model, and opened the dashboard through an SSH tunnel. The visible results are recorded in [AWS evidence](evidence/aws-oct15.md). Full cmx automation remains unfinished. The project still needs Multipass and an OpenStack cloud as well.

## 1. Import the Existing Public Key

The Mac key was created at `~/.ssh/sports_midterm_aws`. Changing the project name does not rename that file. Import only its `.pub` public file into AWS.

In **Mac Terminal**, run:

```bash
pbcopy < ~/.ssh/sports_midterm_aws.pub
```

In the Ohio-region **EC2 → Key pairs → Import key pair** page, set Name to `sports-midterm-aws`. Clear Public key contents, then press Command-V. The pasted text should begin `ssh-ed25519`. The `pbcopy` command itself does not belong in that box. Click Import key pair, then select it in the instance launch page.

The instructor requires passphrases and ssh-agent/Keychain. The 10:43 am Mac screenshot showed a passphrase prompt followed by `Identity added` after `ssh-add --apple-use-keychain`, confirming that this AWS key was unlocked and loaded into the agent. The instructor's full `cmx key scan` and `cmx key github list` outputs still need to be shown separately. Keep the private file and passphrase off GitHub and out of screenshots.

## 2. Launch Settings

| Setting | Value |
| --- | --- |
| Region | Ohio, `us-east-2` |
| Name tag | `SPORTSSTATS` |
| Image | Ubuntu Server **24.04 LTS** |
| Architecture | 64-bit x86 |
| Instance type | t3.micro |
| Key pair | sports-midterm-aws |
| SSH source | My IP |
| HTTP/HTTPS | Leave unchecked for the first test |
| Storage | 8 GiB |
| Instance count | 1 |

The earlier screenshot showed Ubuntu 26.04; select 24.04 to match the project setup. Check the account's Free-plan credit balance before launching. Current costs and limits are in [the appendix](costs.md).

## 3. Connect and Run the Application

After launch, wait for Running and passing status checks. Use the instance's **Connect → SSH client** page to get its actual public address. Ubuntu uses the username `ubuntu`; the Mac private-key path remains `~/.ssh/sports_midterm_aws`. Confirm the host fingerprint through EC2 before accepting an unfamiliar host key.

Transfer tracked project source without data or credentials. A source-only archive can be made in the Mac repository with `git archive`; download the pinned historical dataset inside the guest. Keep the remote project at `~/sports-project` to match the cmx smoke command.

In the guest, from that project directory, the application checks are:

```bash
python3 --version
make -C sports test
make -C sports history
make -C sports model
```

Python 3.12+ is required. Skip `history` after a successful import. Expected data counts are 2,460 team-game rows, 1,230 games, and 30 teams. The Chicago comparison uses 72 games and reports logistic Brier about 0.2533 versus constant 0.2500. Save genuine command output with its environment and time; do not publish key details.

For the first dashboard test, bind the guest server to `127.0.0.1` and use an SSH tunnel from the Mac. This avoids opening dashboard port 8000 to the Internet. This configuration was observed working at 2:28 pm, using Mac port 8001 and guest port 8000. Keep both Terminal sessions open while using the foreground server. The full database totals, lower model comparison, persistent service, and live cmx integration still need direct verification.

## 4. cmx Requirement

`python3 -m sports.cloud plan --cloud aws` prints the commands for `SPORTSSTATS`. It does not run them. Do not run the printed `start` command against a VM already created in the console. The audited upstream AWS provider has unresolved driver/method issues. A successful console deployment would prove the app runs on EC2; live cmx integration remains a separate requirement.

After the provider, source, and data are working, this checks the guest model through cmx:

```bash
python3 -m sports.cloud smoke --cloud aws --name SPORTSSTATS
```

Do not mark it complete without a real successful result. Keep any AWS provider fix separate from the prepared Google-only contribution and open only one upstream PR at a time.

Sources: [EC2 key-pair import](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html), [launch wizard](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-instance-wizard.html), [AWS Free Tier](https://aws.amazon.com/free/free-tier-faqs/), and [Week 7](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/assignments/).

Acknowledgment: OpenAI Codex drafted this guide. Selected settings and observed account status are distinguished from unverified deployment steps.
