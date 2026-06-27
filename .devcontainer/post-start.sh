#!/usr/bin/env bash
set -euo pipefail

# Wait for Docker daemon to become available after container start.
for i in $(seq 1 30); do
  if docker info >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

docker info >/dev/null 2>&1 || {
  echo "Docker daemon is not available after startup."
  exit 1
}

echo "Docker and kind are ready:"
docker --version
kind --version
kubectl version --client=true
helm version --short
opencode --version
