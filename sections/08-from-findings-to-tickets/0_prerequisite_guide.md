# Instructor Prerequisite: Docker Image Build

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through Docker build during the live demo.

**Time Budget:** 2–3 mins

---

## 1) Clean old containers

```bash
docker stop finops-issue-tracker 2>/dev/null || true
docker rm finops-issue-tracker 2>/dev/null || true
```

**What it does:** Removes any leftover tracker container from previous runs.

---

## 2) Inspect the service structure

```bash
ls sections/08-from-findings-to-tickets/service/
```

**What it does:** Shows the service directory — `Dockerfile`, `app/`, `data/`, `requirements.txt`, `start.sh`.

---

## 3) Build the Docker image

```bash
docker build -t finops-issue-tracker:latest sections/08-from-findings-to-tickets/service
```

**What it does:** Builds the tracker image. Takes 30–60 seconds depending on network.

> *Talking point: "The tracker is a standalone FastAPI service. REST for humans, MCP for agents. One container, two interfaces."*

---

## 4) Inspect the agent code

```bash
ls sections/08-from-findings-to-tickets/agent/
```

**What it does:** Shows the minimal agent fork — `mcp_client.py` (from Section 06), `tracker_auditor.py`, `structure.py`, `tracker_client.py`.

---

## 5) Ready to teach

When the image is built, start the live walkthrough with:

- `1_guide.md` — Run the tracker (Video 2)
- `2_guide.md` — API walkthrough + manual curl (Video 3)
- `3_guide.md` — Run agent + verify board (Video 5)

## Cleanup after the session

```bash
docker stop finops-issue-tracker
```

**What it does:** Stops the tracker container.
