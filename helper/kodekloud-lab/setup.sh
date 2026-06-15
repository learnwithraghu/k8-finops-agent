#!/usr/bin/env bash
# helper/kodekloud-lab/setup.sh
# ─────────────────────────────────────────────────────────────────────────────
# Sets up the teaching environment through Section 02a on a cluster that
# already has kubectl and helm installed (e.g. a KodeKloud playground).
#
# Prerequisites:
#   • kubectl is on PATH and already configured to talk to the cluster
#   • helm   is on PATH
#   • This script is run from the repo root (i.e. bash helper/kodekloud-lab/setup.sh)
#
# No arguments required — just run it.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

NAMESPACES=("booking-api" "flight-search" "inventory" "payment" "airline")

# Resolve repo root regardless of where the script is invoked from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# ── Helpers ──────────────────────────────────────────────────────────────────
log()     { echo -e "\033[1;34m[setup]\033[0m $*"; }
success() { echo -e "\033[1;32m[setup]\033[0m ✔ $*"; }
warn()    { echo -e "\033[1;33m[setup]\033[0m ⚠ $*"; }
die()     { echo -e "\033[1;31m[setup]\033[0m ✖ $*" >&2; exit 1; }
sep()     { echo -e "\033[2m────────────────────────────────────────\033[0m"; }
has_cmd() { command -v "$1" > /dev/null 2>&1; }

wait_for_pods() {
  local ns="$1" label="$2" timeout="${3:-120s}"
  log "Waiting for pods · ns=${ns} label=${label} (timeout ${timeout})..."
  kubectl wait pods \
    --namespace "${ns}" \
    --selector  "${label}" \
    --for=condition=Ready \
    --timeout="${timeout}" 2>/dev/null \
    || warn "Some pods in '${ns}' did not reach Ready within ${timeout}. Continuing anyway."
}

# ── Banner ───────────────────────────────────────────────────────────────────
echo
echo "  ┌──────────────────────────────────────────────────┐"
echo "  │  k8-finops-agent  ·  KodeKloud Lab  ·  setup.sh │"
echo "  │  Deploys: Airline App → Payment Gateway (02a)    │"
echo "  └──────────────────────────────────────────────────┘"
echo

# ── Step 1: Validate prerequisites ───────────────────────────────────────────
sep
log "Step 1/4 · Validating prerequisites"

for cmd in kubectl helm; do
  if has_cmd "$cmd"; then
    success "$cmd found"
  else
    die "$cmd is not installed or not on PATH. Please install it first."
  fi
done

# Confirm cluster is reachable
if ! kubectl get nodes > /dev/null 2>&1; then
  die "Cannot reach the cluster. Check your kubeconfig / cluster status."
fi
success "Cluster is reachable"
kubectl get nodes

# ── Step 2: Create namespaces ─────────────────────────────────────────────────
sep
log "Step 2/4 · Creating app namespaces"

for ns in "${NAMESPACES[@]}"; do
  if kubectl get namespace "${ns}" > /dev/null 2>&1; then
    warn "Namespace '${ns}' already exists — skipping"
  else
    kubectl create namespace "${ns}"
    success "Namespace '${ns}' created"
  fi
done

# ── Step 3: Deploy Section 02 — Airline App ──────────────────────────────────
sep
log "Step 3/4 · Deploying Section 02 — Airline App"

kubectl apply -k "${REPO_ROOT}/sections/02-airline-app-deployment/manifests/airline-k8-deployment/"
success "Section 02 manifests applied"

wait_for_pods "booking-api"   "app=booking-api"           "120s"
wait_for_pods "flight-search" "app=flight-search-service" "120s"
wait_for_pods "inventory"     "app=inventory-service"     "120s"
wait_for_pods "payment"       "app=payment-processor"     "120s"

# ── Step 4: Deploy Section 02a — Payment Gateway Down ────────────────────────
sep
log "Step 4/4 · Deploying Section 02a — Payment Gateway (broken API)"

kubectl apply -k "${REPO_ROOT}/sections/02a-payment-gateway-down/manifests/"
success "Section 02a manifests applied"

# UI pod should come up; payment-gateway-api is intentionally at 0 replicas
wait_for_pods "payment" "app=payment-gateway" "120s"

# ── Final summary ─────────────────────────────────────────────────────────────
sep
log "Final validation"
echo

echo "  Cluster nodes:"
kubectl get nodes
echo

echo "  All pods across lesson namespaces:"
kubectl get pods -n booking-api -n flight-search -n inventory -n payment -n airline 2>/dev/null || \
  kubectl get pods -A --field-selector "metadata.namespace!=kube-system,metadata.namespace!=kube-public,metadata.namespace!=kube-node-lease"
echo

echo "  Payment namespace (key for 02a):"
kubectl get all -n payment
echo

sep
success "Environment is ready through Section 02a! 🚀"
echo
echo "  ┌─────────────────────────────────────────────────────────────────┐"
echo "  │  Next steps:                                                    │"
echo "  │   • Port-forward the UI:                                        │"
echo "  │     kubectl port-forward svc/payment-gateway -n payment 8089:80 │"
echo "  │   • Open http://localhost:8089 to see the incident scenario     │"
echo "  │   • Follow guide: sections/02a-payment-gateway-down/guide.md   │"
echo "  │                                                                 │"
echo "  │  For Section 04 (Local Python Agent) in Alpine-based labs:      │"
echo "  │   • Install Python and dependencies:                            │"
echo "  │     apk update && apk add python3 py3-pip && \                  │"
echo "  │     python3 -m venv venv && source venv/bin/activate && \       │"
echo "  │     pip install -r sections/04-local-python-agent/requirements.txt│"
echo "  │                                                                 │"
echo "  │  To tear everything down:                                       │"
echo "  │     bash helper/kodekloud-lab/cleanup.sh                        │"
echo "  └─────────────────────────────────────────────────────────────────┘"
echo
