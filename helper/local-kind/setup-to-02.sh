#!/usr/bin/env bash
# helper/setup-to-02.sh
# ─────────────────────────────────────────────────────────────────────────────
# Spins up the full teaching environment through Section 02a
# (Cluster → Airline App → Payment Gateway Down)
#
# Usage:
#   bash helper/setup-to-02.sh            # interactive
#   bash helper/setup-to-02.sh --yes      # skip prompts
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Config ─────────────────────────────────────────────────────────────────
CLUSTER_NAME="finops-cluster"
NAMESPACES=("booking-api" "flight-search" "inventory" "payment" "airline")
ASSUME_YES=false

# Resolve repo root regardless of where the script is called from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# ── Helpers ─────────────────────────────────────────────────────────────────
log()     { echo -e "\033[1;34m[setup]\033[0m $*"; }
success() { echo -e "\033[1;32m[setup]\033[0m ✔ $*"; }
warn()    { echo -e "\033[1;33m[setup]\033[0m ⚠ $*"; }
die()     { echo -e "\033[1;31m[setup]\033[0m ✖ $*" >&2; exit 1; }
sep()     { echo -e "\033[2m────────────────────────────────────────\033[0m"; }

has_cmd() { command -v "$1" > /dev/null 2>&1; }

confirm() {
  local prompt="$1"
  if [[ "$ASSUME_YES" == true ]]; then return 0; fi
  read -r -p "$prompt [y/N]: " reply
  [[ "$reply" =~ ^[Yy]$ ]]
}

wait_for_pods() {
  local ns="$1"
  local label="$2"
  local timeout="${3:-90s}"
  log "Waiting for pods in namespace '${ns}' (label: ${label}) — timeout ${timeout}..."
  kubectl wait pods \
    --namespace "${ns}" \
    --selector "${label}" \
    --for=condition=Ready \
    --timeout="${timeout}" 2>/dev/null || warn "Some pods in '${ns}' did not reach Ready within ${timeout}. Continuing anyway."
}

# ── Parse args ──────────────────────────────────────────────────────────────
usage() {
  cat <<EOF
Usage: $0 [--yes]

Spins up the teaching environment through Section 02a.

Steps performed:
  1. Validate prerequisites (docker, kind, kubectl, helm)
  2. Create Kind cluster: ${CLUSTER_NAME}
  3. Create app namespaces
  4. Deploy Section 02  — Airline App
  5. Deploy Section 02a — Payment Gateway (broken API)
  6. Final validation summary

Options:
  --yes   Skip confirmation prompts
  -h      Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes) ASSUME_YES=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
  shift
done

# ── Main ────────────────────────────────────────────────────────────────────
main() {
  echo
  echo "  ┌──────────────────────────────────────────────┐"
  echo "  │   k8-finops-agent  ·  setup-to-02.sh        │"
  echo "  │   Spins up: Cluster → Airline App → 02a     │"
  echo "  └──────────────────────────────────────────────┘"
  echo

  if ! confirm "This will create a Kind cluster and deploy all resources up to Section 02a. Proceed?"; then
    log "Cancelled."
    exit 0
  fi

  # ── Step 1: Validate prerequisites ────────────────────────────────────────
  sep
  log "Step 1/5 · Validating prerequisites"

  for cmd in docker kind kubectl helm; do
    if has_cmd "$cmd"; then
      success "$cmd found: $(${cmd} version --short 2>/dev/null || ${cmd} --version 2>/dev/null | head -1)"
    else
      die "$cmd is not installed or not on PATH. Please install it first."
    fi
  done

  # Docker daemon must be running
  if ! docker info > /dev/null 2>&1; then
    die "Docker daemon is not running. Start Docker Desktop and retry."
  fi
  success "Docker daemon is running"

  # ── Step 2: Create Kind cluster ───────────────────────────────────────────
  sep
  log "Step 2/5 · Creating Kind cluster '${CLUSTER_NAME}'"

  if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    warn "Cluster '${CLUSTER_NAME}' already exists — skipping creation"
  else
    kind create cluster --name "${CLUSTER_NAME}"
    success "Cluster '${CLUSTER_NAME}' created"
  fi

  # Set kubectl context
  kubectl cluster-info --context "kind-${CLUSTER_NAME}" > /dev/null
  success "kubectl is talking to kind-${CLUSTER_NAME}"

  # Wait for node to be fully Ready before deploying anything
  log "Waiting for cluster node to be Ready (up to 120s)..."
  kubectl wait node --all --for=condition=Ready --timeout=120s
  success "Cluster node is Ready"

  # ── Step 3: Create namespaces ─────────────────────────────────────────────
  sep
  log "Step 3/5 · Creating app namespaces"

  for ns in "${NAMESPACES[@]}"; do
    if kubectl get namespace "${ns}" > /dev/null 2>&1; then
      warn "Namespace '${ns}' already exists — skipping"
    else
      kubectl create namespace "${ns}"
      success "Namespace '${ns}' created"
    fi
  done

  # ── Step 4: Deploy Section 02 — Airline App ───────────────────────────────
  sep
  log "Step 4/5 · Deploying Section 02 — Airline App"

  kubectl apply -k "${REPO_ROOT}/sections/02-airline-app-deployment/manifests/airline-k8-deployment/"
  success "Section 02 manifests applied"

  # Wait for core services to be ready (120s to account for image pulls on cold cluster)
  wait_for_pods "booking-api"    "app=booking-api"            "120s"
  wait_for_pods "flight-search"  "app=flight-search-service"  "120s"
  wait_for_pods "inventory"      "app=inventory-service"      "120s"
  wait_for_pods "payment"        "app=payment-processor"      "120s"

  # ── Step 5: Deploy Section 02a — Payment Gateway Down ─────────────────────
  sep
  log "Step 5/5 · Deploying Section 02a — Payment Gateway (broken API)"

  kubectl apply -k "${REPO_ROOT}/sections/02a-payment-gateway-down/manifests/"
  success "Section 02a manifests applied"

  # UI pod should come up; API is intentionally at 0 replicas
  wait_for_pods "payment" "app=payment-gateway" "120s"

  # ── Final validation ───────────────────────────────────────────────────────
  sep
  log "Final validation"
  echo

  echo "  Cluster nodes:"
  kubectl get nodes
  echo

  echo "  All pods across lesson namespaces:"
  kubectl get pods -n booking-api -n flight-search -n inventory -n payment -n airline 2>/dev/null || \
    kubectl get pods --field-selector "metadata.namespace!=kube-system,metadata.namespace!=kube-public,metadata.namespace!=kube-node-lease,metadata.namespace!=local-path-storage" -A
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
  echo "  │     kubectl port-forward svc/payment-gateway -n payment 8089:80 --address 0.0.0.0 │"
  echo "  │   • Open http://localhost:8089 to see the incident scenario     │"
  echo "  │   • Follow guide: sections/02a-payment-gateway-down/guide.md   │"
  echo "  │                                                                 │"
  echo "  │  To tear everything down:                                       │"
  echo "  │     bash helper/cleanup.sh                                      │"
  echo "  └─────────────────────────────────────────────────────────────────┘"
  echo
}

main "$@"
