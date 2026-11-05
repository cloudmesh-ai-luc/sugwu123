# Individual Week 5 Participation
Sydel Ugwu

These are drafts and review notes.

## Status

- Implementation: solo.
- Existing contribution: [PR #11](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11).

## Peer-review status at submission

At the October 1 check, my PR #11 was the only open PR in the upstream
repository. I have not completed a posted peer review, so this remains an
unfinished task in my self-assessment. Earlier contributions, including
[PR #3](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/3), were already
merged and remain available to read and comment on. The review notes below
are retained, but they do not establish that feedback was submitted.

The assignment says: "Before implementation discuss on Piazza."
A local candidate has been prepared. Posting now does not establish that
discussion happened before it was prepared; the self-assessment records this
uncertainty honestly.

## Piazza draft

Subject: Week 5 Multipass improvements for my solo sports project

I am working individually on the Multipass provider to support my Sports
Statistics and Probability Analysis Platform. My earlier Mac verification
recorded 8 passes and 3 failures: info and run were not implemented, and start
tried to launch an existing VM.

My contribution adds VM information and guest execution,
resumes existing instances, supports --name without changing the counter, and
exports VM lists as JSON, YAML, CSV, or tables. The updated unit checks passed
117 tests, excluding the separate CMC integration. The real Mac verification
recorded 50 passed and 0 failed for the selected Multipass scope. I also checked
ssh and login manually; both returned the expected hostname and ubuntu user,
and exited back to my Mac. Those two checks are separate from the 50-check log.

For shelve/unshelve, the provider reports that Multipass does not support
OpenStack shelving and documents suspend/start separately. I would appreciate
feedback on that behavior and any overlap with other students' provider work.
My existing contribution is PR #11:
https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11

Report and verification evidence:
https://github.com/cloudmesh-ai-luc/sugwu123/blob/main/assignments/week5/README.md

## Peer review notes

Reviewed the published diff of
[PR #3, Add VM command verification script](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/3)
by kbass-maker. It was already merged when these notes were prepared.
This is a source review, not a live OpenStack test.

Positive: the script distinguishes skips and requires an explicit lifecycle
mode before running mutating commands.

Concrete follow-up observations:

1. With a VM name, safe mode invokes login. A provider implementing an
   interactive guest shell can block an unattended run. Make that a manual
   check or clearly separate it from noninteractive verification.
2. The script passes the VM name to ssh-config, but the current CLI accepts
   no positional name. That invocation fails before provider behavior is tested.
3. Lifecycle mode stops the VM before suspending it. Resume it before suspend,
   then assert the state. Multipass reset restarts the daemon and does not
   isolate its effect to the dedicated VM.
4. Help checks confirm command availability. They do not demonstrate that the
   corresponding operation works.

## Suggested peer comment

The safe default and separate skipped count make the script useful. I noticed
that the VM-specific path calls login, which can open an interactive shell, and
passes a VM name to ssh-config even though that command currently takes no
positional argument. In the lifecycle path, I suggest checking state and
resuming the VM between stop and suspend. Multipass reset also acts on the
daemon, so it should be separate from the dedicated-VM tests. These observations
come from reviewing the diff and current CLI signatures; I have not run this
script against OpenStack.

Read the diff and these observations yourself before posting. This document
is not evidence that a student comment or review was submitted.
