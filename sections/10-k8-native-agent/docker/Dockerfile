# Dockerfile for Section 10: Kubernetes-Native FinOps Agent
#
# Build context must be the section folder so both agent/ and config/ are
# available. The image uses the same agent code as the MCP-agent track (Sections 06 and 07) but is
# packaged to run inside the cluster via a CronJob.

FROM python:3.12-slim

# Copy build-time requirements (relative to the section root build context).
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the agent package and its config.
COPY agent /app/agent
COPY config /app/config

WORKDIR /app

# Run the agent. In Kubernetes, env vars come from the Secret + ConfigMap.
CMD ["python", "-m", "agent.main"]
