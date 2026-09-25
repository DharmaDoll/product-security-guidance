#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
EXPECTED_CONTEXT=${PSB_TEST_CONTEXT:-}
NAMESPACE=psb-resource-test
POLICY=psb-resource-bounds.example.com
ERROR_FILE=${TMPDIR:-/tmp}/psb-resource-bounds-errors.$$

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

if kubectl --context "$EXPECTED_CONTEXT" get namespace "$NAMESPACE" >/dev/null 2>&1; then
  echo "ERROR namespace '$NAMESPACE' already exists; refusing to modify or delete it" >&2
  exit 2
fi

if kubectl --context "$EXPECTED_CONTEXT" get validatingadmissionpolicy "$POLICY" >/dev/null 2>&1 ||
  kubectl --context "$EXPECTED_CONTEXT" get validatingadmissionpolicybinding "$POLICY" >/dev/null 2>&1; then
  echo "ERROR admission policy '$POLICY' already exists; refusing to modify or delete it" >&2
  exit 2
fi

cleanup() {
  kubectl --context "$EXPECTED_CONTEXT" delete -f "$SCRIPT_DIR/admission-policy.yaml" \
    --ignore-not-found --wait=false >/dev/null 2>&1 || true
  kubectl --context "$EXPECTED_CONTEXT" delete -f "$SCRIPT_DIR/namespace.yaml" \
    --ignore-not-found --wait=false >/dev/null 2>&1 || true
  rm -f "$ERROR_FILE"
}
trap cleanup EXIT HUP INT TERM

expect_rejected() {
  manifest=$1
  marker=$2
  description=$3
  attempts=0
  while [ "$attempts" -lt 20 ]; do
    if kubectl --context "$EXPECTED_CONTEXT" create --dry-run=server -f "$manifest" \
      >/dev/null 2>"$ERROR_FILE"; then
      attempts=$((attempts + 1))
      sleep 1
      continue
    fi
    if grep -F "$marker" "$ERROR_FILE" >/dev/null; then
      echo "PASS $description"
      return 0
    fi
    cat "$ERROR_FILE" >&2
    echo "FAIL $description returned an unexpected error" >&2
    exit 1
  done
  echo "FAIL $description was accepted" >&2
  exit 1
}

kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/namespace.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/admission-policy.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/resource-quota.yaml" >/dev/null

expect_rejected \
  "$SCRIPT_DIR/reject-missing-resource.yaml" \
  "All regular and init containers must declare CPU memory and ephemeral-storage requests and limits" \
  "missing ephemeral-storage budget denied"

kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/workload.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" wait --for=condition=Ready pod/bounded \
  -n "$NAMESPACE" --timeout=60s >/dev/null

QOS_CLASS=$(kubectl --context "$EXPECTED_CONTEXT" get pod bounded -n "$NAMESPACE" \
  -o jsonpath='{.status.qosClass}')
if [ "$QOS_CLASS" != "Guaranteed" ]; then
  echo "FAIL bounded Pod QoSClass is '$QOS_CLASS', expected 'Guaranteed'" >&2
  exit 1
fi
echo "PASS bounded Pod has Guaranteed QoS"

USED_CPU=$(kubectl --context "$EXPECTED_CONTEXT" get resourcequota psb-resource-budget \
  -n "$NAMESPACE" -o jsonpath='{.status.used.requests\.cpu}')
USED_MEMORY=$(kubectl --context "$EXPECTED_CONTEXT" get resourcequota psb-resource-budget \
  -n "$NAMESPACE" -o jsonpath='{.status.used.requests\.memory}')
USED_STORAGE=$(kubectl --context "$EXPECTED_CONTEXT" get resourcequota psb-resource-budget \
  -n "$NAMESPACE" -o jsonpath='{.status.used.requests\.ephemeral-storage}')

if [ "$USED_CPU" != "250m" ] || [ "$USED_MEMORY" != "64Mi" ] || [ "$USED_STORAGE" != "128Mi" ]; then
  echo "FAIL quota usage mismatch: cpu=$USED_CPU memory=$USED_MEMORY ephemeral-storage=$USED_STORAGE" >&2
  exit 1
fi
echo "PASS quota usage records the admitted Pod budget"

expect_rejected \
  "$SCRIPT_DIR/reject-over-quota.yaml" \
  "exceeded quota: psb-resource-budget" \
  "aggregate CPU request above namespace quota denied"
