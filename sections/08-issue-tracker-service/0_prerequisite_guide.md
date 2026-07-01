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
ls sections/08-issue-tracker-service/service/
```

**What it does:** Shows the service directory — `Dockerfile`, `app/`, `data/`, `requirements.txt`, `start.sh`.

---

## 3) Build the Docker image

```bash
docker build -t finops-issue-tracker:latest sections/08-issue-tracker-service/service
```

**What it does:** Builds the tracker image. Takes 30–60 seconds depending on network.

> *Talking point: "The tracker is a standalone FastAPI service. REST for humans, MCP for agents. One container, two interfaces."*

---

## 4) Ready to teach

When the image is built, start the live walkthrough with:

- `1_guide.md` — Run the tracker
- `2_guide.md` — Create tickets via REST

## Cleanup after the session

```bash
docker stop finops-issue-tracker
```

**What it does:** Stops the tracker container.
