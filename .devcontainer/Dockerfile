FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG KIND_VERSION=v0.24.0
ARG KUBECTL_VERSION=v1.31.2
ARG HELM_VERSION=v3.16.1
ARG TARGETARCH

RUN set -eux; \
    case "${TARGETARCH}" in \
      "amd64") kind_arch="amd64" ;; \
      "arm64") kind_arch="arm64" ;; \
      *) echo "Unsupported TARGETARCH: ${TARGETARCH}"; exit 1 ;; \
    esac; \
    curl -fsSL -o /usr/local/bin/kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-${kind_arch}"; \
    chmod +x /usr/local/bin/kind; \
    kind --version; \
    curl -fsSL -o /usr/local/bin/kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${kind_arch}/kubectl"; \
    chmod +x /usr/local/bin/kubectl; \
    kubectl version --client=true; \
    curl -fsSL "https://get.helm.sh/helm-${HELM_VERSION}-linux-${kind_arch}.tar.gz" -o /tmp/helm.tgz; \
    tar -xzf /tmp/helm.tgz -C /tmp; \
    mv /tmp/linux-${kind_arch}/helm /usr/local/bin/helm; \
    chmod +x /usr/local/bin/helm; \
    rm -rf /tmp/helm.tgz /tmp/linux-${kind_arch}; \
    helm version --short
