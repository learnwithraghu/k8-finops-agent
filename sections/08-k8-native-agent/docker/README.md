# Docker

This folder contains the container build for the Section 08 Kubernetes-native agent.

## Files
- `Dockerfile` — builds `finops-agent:latest` from the Section 05 agent code
- `requirements.txt` — minimal Python dependencies for the agent
- `.dockerignore` — excludes `.env`, manifests, and build artifacts from the image context

## Build
Run from the section root:

```bash
cd sections/08-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
```

## Kind load
If you are using Kind, load the image into the cluster:

```bash
kind load docker-image finops-agent:latest --name <your-cluster-name>
```

## Important
The Dockerfile does **not** copy `.env` or embed the LLM API key. The key is injected at runtime through the Kubernetes Secret defined in `manifests/secret.yaml` (placeholder) or created via `kubectl create secret`.
