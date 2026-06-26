# KodeKloud Lab - Setup Guide

Run these **3 scripts in order** from the repo root to get the full environment ready.

---

## Script 1 — Install Docker

Installs Docker, starts the service, and verifies it works.
Automatically detects your OS (Alpine, Ubuntu/Debian, CentOS/RHEL, or macOS).

```bash
bash helper/kodekloud-lab/install-docker.sh
```

What it does:
1. Detects your OS
2. Installs Docker (and Docker Compose on Alpine)
3. Starts the Docker service
4. Verifies by running `hello-world`

---

## Script 2 — Deploy the Cluster & Airline App

Sets up the teaching environment through Section 02a:
creates namespaces, deploys the airline app, and deploys the payment gateway (broken API scenario).

```bash
bash helper/kodekloud-lab/setup.sh
```

What it does:
1. Validates `kubectl` and `helm` are on PATH
2. Confirms the cluster is reachable
3. Creates all lesson namespaces
4. Deploys Section 02 — Airline App
5. Deploys Section 02a — Payment Gateway (broken API)

---

## Script 3 — Install Python & Agent Dependencies

Installs Python 3 and pip (on Alpine), creates a virtual environment, and
installs the Python packages needed for Sections 04 and 05.

```bash
bash helper/kodekloud-lab/install-python.sh
```

What it does:
1. Installs `python3` and `py3-pip` via `apk` (Alpine) or validates existing Python
2. Creates a virtual environment at `venv/`
3. Activates the virtual environment
4. Installs Section 04 dependencies (`kubernetes`, `pyyaml`, `python-dotenv`)
5. Installs Section 08 dependencies (`langchain`, `langchain-openai`, `pydantic`)

> **Note:** After a new shell session, re-activate the venv with:
> ```bash
> source venv/bin/activate
> ```

---

## Teardown

To remove everything deployed by `setup.sh`:

```bash
bash helper/kodekloud-lab/cleanup.sh
```
