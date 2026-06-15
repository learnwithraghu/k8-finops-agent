#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="finops-cluster"
NAMESPACES=("airline" "booking-api" "flight-search" "inventory" "payment" "tech-debt")
IMAGE_PATTERNS=("k8-finops-agent" "issue-tracker")
AGGRESSIVE=false
ASSUME_YES=false

usage() {
  cat <<EOF
Usage: $0 [--yes] [--aggressive]

Cleans up the local teaching environment for this repo.

Options:
  --yes         Skip confirmation prompts
  --aggressive  Also prune unused Docker data (volumes/networks/images)
EOF
}

confirm() {
  local prompt="$1"
  if [[ "$ASSUME_YES" == true ]]; then
    return 0
  fi
  read -r -p "$prompt [y/N]: " reply
  [[ "$reply" =~ ^[Yy]$ ]]
}

log() { echo "[cleanup] $*"; }
warn() { echo "[cleanup] WARNING: $*"; }

has_cmd() { command -v "$1" >/dev/null 2>&1; }

cleanup_k8s() {
  if ! has_cmd kubectl; then
    warn "kubectl not found; skipping Kubernetes cleanup"
    return
  fi

  log "Removing Section 02 app manifests if the cluster is still available..."
  kubectl delete -k sections/02-airline-app-deployment/manifests/airline-k8-deployment --ignore-not-found=true >/dev/null 2>&1 || true

  log "Deleting lesson namespaces..."
  for ns in "${NAMESPACES[@]}"; do
    kubectl delete namespace "$ns" --ignore-not-found=true >/dev/null 2>&1 || true
  done

  log "Deleting Kind cluster ${CLUSTER_NAME} if present..."
  if has_cmd kind; then
    kind delete cluster --name "$CLUSTER_NAME" >/dev/null 2>&1 || true
  fi
}

cleanup_docker() {
  if ! has_cmd docker; then
    warn "docker not found; skipping Docker cleanup"
    return
  fi

  log "Stopping/removing containers from project images..."
  for pattern in "${IMAGE_PATTERNS[@]}"; do
    docker ps -aq --filter "ancestor=${pattern}" | xargs -r docker rm -f >/dev/null 2>&1 || true
  done

  log "Removing project images..."
  for pattern in "${IMAGE_PATTERNS[@]}"; do
    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | awk -v p="$pattern" '$1 ~ p {print $2}' | xargs -r docker rmi -f >/dev/null 2>&1 || true
    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | awk -v p="$pattern" '$1 ~ p {print $2}' | xargs -r docker rmi -f >/dev/null 2>&1 || true
  done

  if [[ "$AGGRESSIVE" == true ]]; then
    log "Aggressively pruning unused Docker data..."
    docker system prune -af --volumes >/dev/null 2>&1 || true
  else
    log "Pruning dangling Docker data only..."
    docker image prune -f >/dev/null 2>&1 || true
    docker container prune -f >/dev/null 2>&1 || true
  fi
}

main() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --yes) ASSUME_YES=true ;;
      --aggressive) AGGRESSIVE=true ;;
      -h|--help) usage; exit 0 ;;
      *) echo "Unknown option: $1"; usage; exit 1 ;;
    esac
    shift
  done

  echo "This will clean up local resources for the k8-finops-agent teaching flow."
  echo "Targets: Kind cluster, lesson namespaces, project images, and Docker cleanup."
  if ! confirm "Proceed?"; then
    log "Cancelled"
    exit 0
  fi

  cleanup_k8s
  cleanup_docker

  log "Done."
}

main "$@"
