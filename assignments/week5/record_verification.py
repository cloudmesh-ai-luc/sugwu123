#!/usr/bin/env python3
"""Record the actual Mac verifier log while leaving skipped tasks unchecked."""
import argparse
from datetime import datetime
from pathlib import Path
import re

REQUIRED_CHECKS = [
    "Start with --name",
    "Explicit name does not increment counter",
    "VM info",
    "Guest hostname",
    "Successful command with no output",
    "Failed guest command returns nonzero",
    "List format table", "List format json", "List format yaml", "List format csv",
    "Restart running VM", "Running state after restart",
    "Stop VM", "Stopped state",
    "Start existing VM", "Running state after start",
    "Suspend VM", "Suspended state",
    "Resume suspended VM", "Running state after resume",
    "Explicit start and resume keep counter unchanged",
    "Automatic naming sequence 1", "Persisted counter 1",
    "Automatic naming sequence 2", "Persisted counter 2",
    "Other VM inventory and states preserved",
]


def main():
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", nargs="?", type=Path, default=directory / "verification-week5.txt")
    arguments = parser.parse_args()
    log = arguments.log.read_text()
    summaries = re.findall(r"^Results: (\d+) passed, (\d+) failed$", log, re.MULTILINE)
    if not summaries:
        parser.error("No verification summary found; retain the complete script output.")
    passed, failed = map(int, summaries[-1])
    missing = [label for label in REQUIRED_CHECKS if f"PASS: {label}" not in log]
    verified = failed == 0 and passed >= 50 and not missing
    failures = re.findall(r"^FAIL: (.+)$", log, re.MULTILINE)
    recorded_at = datetime.now().astimezone().isoformat(timespec="seconds")
    details = [
        "## Latest Mac verification", "",
        f"Recorded from [{arguments.log.name}]({arguments.log.name}) at {recorded_at}.",
        f"Actual script summary: **{passed} passed, {failed} failed**.", "",
    ]
    if verified:
        details.append("The required lifecycle, naming, list-format, and inventory-preservation checks passed.")
        details.append("This confirms the script's selected Multipass scope, including expected-error checks.")
    else:
        details.append("The complete selected scope is not marked verified.")
        if failures:
            details.extend(["", "Failed checks:", "", *[f"- {label}" for label in failures]])
        if missing:
            details.extend(["", "Missing successful checks:", "", *[f"- {label}" for label in missing]])
    details.extend([
        "",
        "Interactive shells, daemon reset, CMC integration, remaining CLI gaps,",
        "other providers, and class participation are still separate tasks.",
        "Unsupported shelving checks are not successful shelving operations.",
        "",
    ])
    readme = directory / "README.md"
    report = readme.read_text()
    report = re.sub(
        r"^\| Latest Mac run \|.*$",
        f"| Latest Mac run | {passed} passed, {failed} failed | [Actual host log]({arguments.log.name}); selected scope {'verified' if verified else 'incomplete'}. |",
        report, flags=re.MULTILINE,
    )
    report = re.sub(r"^## Latest Mac verification\n.*?(?=^## |\Z)",
                    "\n".join(details), report, flags=re.MULTILINE | re.DOTALL)
    if verified:
        report = report.replace("Live verification is a separate remaining step.",
                                "Live verification is recorded below.")
        report = report.replace("Live verification is incomplete; see the latest log.",
                                "Live verification is recorded below.")
        report = report.replace(
            "The main unresolved item is live Mac verification of the follow-up repairs.",
            "The selected Multipass Mac verification is recorded above."
        )
        report = report.replace("The selected Multipass Mac verification is incomplete; see the latest log.",
                                "The selected Multipass Mac verification is recorded above.")
    else:
        report = report.replace("Live verification is recorded below.",
                                "Live verification is incomplete; see the latest log.")
        report = report.replace("The selected Multipass Mac verification is recorded above.",
                                "The selected Multipass Mac verification is incomplete; see the latest log.")
    report = re.sub(r"(Implemented and regression-tested; )(?:Mac rerun pending|Verified in the latest Mac log|Mac rerun incomplete)\.",
                    r"\g<1>" + ("Verified in the latest Mac log." if verified else "Mac rerun incomplete."), report)
    readme.write_text(report)
    root_readme = directory.parents[1] / "README.md"
    root = root_readme.read_text()
    label = "Verify Multipass lifecycle, naming, and list formats on Mac."
    root = re.sub(r"- \[[ x]\] " + re.escape(label),
                  f"- [{'x' if verified else ' '}] {label}", root)
    root_readme.write_text(root)
    pr_path = directory / "pr-update.md"
    pr = pr_path.read_text()
    pr = re.sub(r"^Live Mac verification:.*$",
                f"Live Mac verification: {passed} passed, {failed} failed; selected scope {'verified' if verified else 'incomplete'}.",
                pr, flags=re.MULTILINE)
    pr_path.write_text(pr)
    print(f"Recorded {passed} passed, {failed} failed; selected scope {'verified' if verified else 'incomplete'}.")
    print("Full command coverage and participation checkboxes remain unchanged.")


if __name__ == "__main__":
    main()
