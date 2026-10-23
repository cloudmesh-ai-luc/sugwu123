# October 15 Mac Evidence

The accessible screenshot labeled October 15, 2026, 8:30:06 am shows `make -C sports test` finishing on the student's Mac:

```text
Ran 34 tests in 1.338s

OK
```

This is a transcription of visible output, not a new terminal log. The earlier 8:28 am screenshot shows the imported `midterm/oct15-prep` branch at `e73bdbf`. These observations support the Mac test result for that version. They do not establish that the later AWS-plan update was applied or tested there.

The historical-data import, model output, dashboard, current VM service, and live remote-cloud runs have not been observed on the Mac in the reviewed screenshots. October 1 synthetic VM evidence remains separate in [VM deployment](../vm-deployment.md).

The AWS account screen showed a Free plan and $100 credits. At 9:18 am, key import failed because a shell command had been pasted into the public-key box. The 9:21 am screenshot shows the correct Mac copy command completed. The 9:25 am screenshot shows **Successfully imported key pair**, with `sports-midterm-aws` listed as Ed25519. This confirms public-key import, not a nonempty private-key passphrase or a launched VM. No private key, account identifier, or account screenshot is included here.

Acknowledgment: OpenAI Codex inspected the accessible screenshots and drafted this evidence note. Only visible results are marked confirmed.
