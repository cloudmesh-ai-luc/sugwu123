#!/usr/bin/env bash
# Sydel Ugwu
# Run the disposable verifier maintained with the VM implementation.
set -uo pipefail

VM_REPO="${CLOUDMESH_VM_REPO:-$HOME/Desktop/cloudmesh-ai-vm}"
VERIFY_SCRIPT="$VM_REPO/tests/bin/verify_multipass_week5.sh"
if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "Missing verifier: $VERIFY_SCRIPT"
    echo "Apply the Week 5 fixes on feature/week5-multipass first."
    echo "Set CLOUDMESH_VM_REPO if your checkout is elsewhere."
    exit 2
fi

bash "$VERIFY_SCRIPT"
