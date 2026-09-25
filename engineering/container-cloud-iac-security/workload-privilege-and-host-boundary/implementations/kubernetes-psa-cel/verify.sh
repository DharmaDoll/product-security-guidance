#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
EXPECTED_CONTEXT=${PSB_TEST_CONTEXT:-}

if ! command -v kubectl >/dev/null 2>&1; then
  echo "ERROR kubectl is required" >&2
  exit 2
fi

CURRENT_CONTEXT=$(kubectl config current-context)

if [ -z "$EXPECTED_CONTEXT" ]; then
  echo "ERROR set PSB_TEST_CONTEXT to the disposable cluster context" >&2
  exit 2
fi

if [ "$CURRENT_CONTEXT" != "$EXPECTED_CONTEXT" ]; then
  echo "ERROR current context '$CURRENT_CONTEXT' does not match PSB_TEST_CONTEXT '$EXPECTED_CONTEXT'" >&2
  exit 2
fi

cleanup() {
  kubectl --context "$EXPECTED_CONTEXT" delete -f "$SCRIPT_DIR/admission-policy.yaml" --ignore-not-found >/dev/null 2>&1 || true
  kubectl --context "$EXPECTED_CONTEXT" delete -f "$SCRIPT_DIR/namespace.yaml" --ignore-not-found >/dev/null 2>&1 || true
}
trap cleanup EXIT HUP INT TERM

kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/admission-policy.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/namespace.yaml" >/dev/null

wait_for_policy() {
  attempts=0
  while [ "$attempts" -lt 15 ]; do
    output_file=$(mktemp)
    if ! kubectl --context "$EXPECTED_CONTEXT" create --dry-run=server \
      -f "$SCRIPT_DIR/fixtures/ambient-token-pod.yaml" >"$output_file" 2>&1 &&
      grep -Fq "Disable automatic service account token mounting" "$output_file"; then
      rm -f "$output_file"
      return 0
    fi
    rm -f "$output_file"
    attempts=$((attempts + 1))
    sleep 1
  done
  echo "FAIL admission policy did not become observable within 15 seconds" >&2
  exit 1
}

wait_for_policy

if kubectl --context "$EXPECTED_CONTEXT" create --dry-run=server -f "$SCRIPT_DIR/fixtures/secure-pod.yaml" >/dev/null; then
  echo "PASS secure pod accepted"
else
  echo "FAIL secure pod rejected" >&2
  exit 1
fi

expect_rejection() {
  fixture=$1
  description=$2
  expected_message=$3
  output_file=$(mktemp)
  if kubectl --context "$EXPECTED_CONTEXT" create --dry-run=server -f "$fixture" >"$output_file" 2>&1; then
    rm -f "$output_file"
    echo "FAIL $description accepted" >&2
    exit 1
  fi
  if ! grep -Fq "$expected_message" "$output_file"; then
    echo "FAIL $description was rejected for an unexpected reason" >&2
    cat "$output_file" >&2
    rm -f "$output_file"
    exit 1
  fi
  rm -f "$output_file"
  echo "PASS $description rejected"
}

expect_rejection "$SCRIPT_DIR/fixtures/privileged-pod.yaml" "privileged pod" "violates PodSecurity"
expect_rejection "$SCRIPT_DIR/fixtures/writable-root-pod.yaml" "writable root filesystem" "Every application container must use a read-only root filesystem"
expect_rejection "$SCRIPT_DIR/fixtures/ambient-token-pod.yaml" "ambient service account token" "Disable automatic service account token mounting"
