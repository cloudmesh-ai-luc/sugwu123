# October 15 AWS Evidence

These observations come from screenshots supplied by Sydel Ugwu. Times are in America/Chicago. Commands were run by the student on the Mac and the Ubuntu EC2 instance; this note records visible results.

| Time | Observed result |
| --- | --- |
| 10:43 am | The Mac requested the AWS private key's passphrase and printed `Identity added` after `ssh-add --apple-use-keychain`. |
| 2:15 pm | SSH reached an Ubuntu shell on the EC2 instance. |
| 2:17 pm | Installation of the required command-line tools completed and the Ubuntu prompt returned. |
| 2:19 pm | The Mac transferred `SPORTSSTATS.tar` to EC2 at 100%. The archive was created from committed `sports` source. |
| 2:20 pm | `make -C sports test` completed in `/home/ubuntu/sports-project`: **34 tests in 1.719 seconds, OK**. |
| 2:22 pm | The historical model command completed and returned to the Ubuntu prompt. The screenshot shows the end of the JSON output, including the April 15, 2015 Chicago game. |
| 2:26 pm | The historical-data dashboard server started on EC2 at `127.0.0.1:8000`. |
| 2:28 pm | Chrome opened the dashboard through the Mac SSH tunnel at `127.0.0.1:8001`. Imported FiveThirtyEight data and the Chicago analysis were visible. |

The visible Chicago selection used all opponents and a 100.5-point threshold. It showed 43 of 82 games above the threshold (52.4%), a 95% Wilson interval of 41.8% to 62.9%, 100.8 average points, and a 50-win, 32-loss record. These values match the prepared historical analysis. They do not establish future prediction accuracy.

The 2:28 pm screenshot does not show the lower machine-learning comparison or all database totals. Those results still need a direct check. The displayed page also retains its earlier heading; the SPORTSSTATS branding change has not been observed on this deployment.

This evidence confirms a working EC2 application reached through SSH. It does not confirm a persistent service, automated VM provisioning through cmx, a current Chameleon application deployment, billing alarms, or the instructor's `cmx key scan` and `cmx key github list` demonstrations. Those checks remain separate.

Acknowledgment: OpenAI Codex inspected the screenshots and drafted this note.
