#!/usr/bin/env bash
# helper/kodekloud-lab/cleanup.sh
# ─────────────────────────────────────────────────────────────────────────────
# Tears down everything deployed by setup.sh on the KodeKloud lab cluster.
# Removes all lesson namespaces and their workloads.
#
# No arguments required — just run it.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

NAMESPACES=("airline" "booking-api" "flight-search" "inventory" "payment" "tech-debt")

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# ── Helpers ──────────────────────────────────────────────────────────────────
log()     { echo -e "\033[1;34m[cleanup]\033[0m $*"; }
success() { echo -e "\033[1;32m[cleanup]\033[0m ✔ $*"; }
warn()    { echo -e "\033[1;33m[cleanup]\033[0m ⚠ $*"; }
die()     { echo -e "\033[1;31m[cleanup]\033[0m ✖ $*" >&2; exit 1; }
sep()     { echo -e "\033[2m────────────────────────────────────────\033[0m"; }
has_cmd() { command -v "$1" > /dev/null 2>&1; }

# ── Banner ───────────────────────────────────────────────────────────────────
echo
echo "  ┌────────────────────────────────────────────────────┐"
echo "  │  k8-finops-agent  ·  KodeKloud Lab  ·  cleanup.sh │"
echo "  │  Removes all lesson namespaces and workloads       │"
echo "  └────────────────────────────────────────────────────┘"
echo

# ── Validate prerequisites ────────────────────────────────────────────────────
sep
log "Validating prerequisites"

if ! has_cmd kubectl; then
  die "kubectl is not installed or not on PATH."
fi

if ! kubectl get nodes > /dev/null 2>&1; then
  die "Cannot reach the cluster. Check your kubeconfig / cluster status."
fi
success "Cluster is reachable"

# ── Remove Section 02a manifests ─────────────────────────────────────────────
sep
log "Removing Section 02a manifests (payment-gateway-down)..."
kubectl delete -k "${REPO_ROOT}/sections/02a-payment-gateway-down/manifests/" \
  --ignore-not-found=true > /dev/null 2>&1 || true
success "Section 02a manifests removed"

# ── Remove Section 02 manifests ──────────────────────────────────────────────
log "Removing Section 02 manifests (airline-app)..."
kubectl delete -k "${REPO_ROOT}/sections/02-airline-app-deployment/manifests/airline-k8-deployment/" \
  --ignore-not-found=true > /dev/null 2>&1 || true
success "Section 02 manifests removed"

# ── Delete lesson namespaces ──────────────────────────────────────────────────
sep
log "Deleting lesson namespaces..."

for ns in "${NAMESPACES[@]}"; do
  if kubectl get namespace "${ns}" > /dev/null 2>&1; then
    kubectl delete namespace "${ns}" --ignore-not-found=true > /dev/null 2>&1 || true
    success "Namespace '${ns}' deleted"
  else
    warn "Namespace '${ns}' not found — skipping"
  fi
done

# ── Final state ───────────────────────────────────────────────────────────────
sep
log "Remaining cluster namespaces:"
kubectl get namespaces
echo

success "Cleanup complete. The cluster is back to its original state."
echo
