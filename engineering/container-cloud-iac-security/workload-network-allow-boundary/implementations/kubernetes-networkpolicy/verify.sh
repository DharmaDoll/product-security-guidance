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

for namespace in psb-net-client psb-net-server psb-net-untrusted; do
  if kubectl --context "$EXPECTED_CONTEXT" get namespace "$namespace" >/dev/null 2>&1; then
    echo "ERROR namespace '$namespace' already exists; refusing to modify or delete it" >&2
    exit 2
  fi
done

cleanup() {
  kubectl --context "$EXPECTED_CONTEXT" delete -f "$SCRIPT_DIR/namespaces.yaml" \
    --ignore-not-found --wait=false >/dev/null 2>&1 || true
}
trap cleanup EXIT HUP INT TERM

connect() {
  source_namespace=$1
  source_pod=$2
  destination_ip=$3
  kubectl --context "$EXPECTED_CONTEXT" --request-timeout=10s \
    exec -n "$source_namespace" "$source_pod" -- \
    /agnhost connect --timeout=2s --protocol=tcp "$destination_ip:8080" \
    >/dev/null 2>&1
}

exec_healthy() {
  source_namespace=$1
  source_pod=$2
  kubectl --context "$EXPECTED_CONTEXT" --request-timeout=10s \
    exec -n "$source_namespace" "$source_pod" -- /agnhost --help \
    >/dev/null 2>&1
}

wait_for_success() {
  source_namespace=$1
  source_pod=$2
  destination_ip=$3
  description=$4
  attempts=0
  while [ "$attempts" -lt 20 ]; do
    if connect "$source_namespace" "$source_pod" "$destination_ip"; then
      return 0
    fi
    attempts=$((attempts + 1))
    sleep 1
  done
  echo "FAIL $description did not become reachable" >&2
  exit 1
}

wait_for_denial() {
  source_namespace=$1
  source_pod=$2
  destination_ip=$3
  description=$4
  attempts=0
  while [ "$attempts" -lt 20 ]; do
    if ! connect "$source_namespace" "$source_pod" "$destination_ip" &&
      exec_healthy "$source_namespace" "$source_pod"; then
      return 0
    fi
    attempts=$((attempts + 1))
    sleep 1
  done
  echo "FAIL $description remained reachable or the source exec path was unhealthy" >&2
  exit 1
}

exercise_allow_removal() {
  policy_file=$1
  source_namespace=$2
  source_pod=$3
  destination_ip=$4
  description=$5

  kubectl --context "$EXPECTED_CONTEXT" apply -f "$policy_file" >/dev/null
  wait_for_success "$source_namespace" "$source_pod" "$destination_ip" "$description temporary allow"

  kubectl --context "$EXPECTED_CONTEXT" delete -f "$policy_file" >/dev/null
  wait_for_denial "$source_namespace" "$source_pod" "$destination_ip" "$description removal"

  kubectl --context "$EXPECTED_CONTEXT" apply -f "$policy_file" >/dev/null
  wait_for_success "$source_namespace" "$source_pod" "$destination_ip" "$description re-allow"

  kubectl --context "$EXPECTED_CONTEXT" delete -f "$policy_file" >/dev/null
  wait_for_denial "$source_namespace" "$source_pod" "$destination_ip" "$description final removal"
}

kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/namespaces.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/default-deny.yaml" >/dev/null
kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/workloads.yaml" >/dev/null

for namespace in psb-net-client psb-net-server psb-net-untrusted; do
  kubectl --context "$EXPECTED_CONTEXT" wait --for=condition=Ready pod --all \
    -n "$namespace" --timeout=60s >/dev/null
done

API_IP=$(kubectl --context "$EXPECTED_CONTEXT" get pod api -n psb-net-server -o jsonpath='{.status.podIP}')
OTHER_IP=$(kubectl --context "$EXPECTED_CONTEXT" get pod other -n psb-net-server -o jsonpath='{.status.podIP}')

if [ -z "$API_IP" ] || [ -z "$OTHER_IP" ]; then
  echo "FAIL server Pod IP was not assigned" >&2
  exit 1
fi

kubectl --context "$EXPECTED_CONTEXT" apply -f "$SCRIPT_DIR/allow.yaml" >/dev/null
wait_for_success psb-net-client client "$API_IP" "authorized client to api flow"
echo "PASS authorized client to api flow allowed"

exercise_allow_removal \
  "$SCRIPT_DIR/probe-allow-client-other-egress.yaml" \
  psb-net-client client "$OTHER_IP" "client egress"
echo "PASS client egress removal denied client to other"

exercise_allow_removal \
  "$SCRIPT_DIR/probe-allow-untrusted-api-ingress.yaml" \
  psb-net-untrusted untrusted "$API_IP" "api ingress"
echo "PASS api ingress removal denied untrusted to api"

wait_for_success psb-net-client client "$API_IP" "authorized client to api flow after probes"
echo "PASS authorized client to api flow remained allowed"
