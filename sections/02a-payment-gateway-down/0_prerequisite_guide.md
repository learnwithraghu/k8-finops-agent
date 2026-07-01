# Instructor Prerequisite: Payment Gateway Setup

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through deployment during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm Section 01 and Section 02 are complete:

- Kind cluster `finops-cluster` is running
- `kubectl` works against the cluster
- Airline app namespaces exist (including `payment` from Section 02)

Quick check:

```bash
kubectl cluster-info
kubectl get namespaces
```

**What it does:** Verifies cluster connectivity and that expected namespaces (e.g. `booking-api`, `payment`) are present.

---

## 1) Deploy the payment gateway (broken API state)

From the repo root:

```bash
kubectl apply -k sections/02a-payment-gateway-down/manifests/
```

**What it does:** Applies the AirPay UI and API via Kustomize into the `payment` namespace. The API Deployment is intentionally set to **0 replicas** — that is the incident you will debug live.

Confirm resources exist:

```bash
kubectl get all -n payment
```

**What it does:** Lists pods, services, and deployments in `payment`. You should see the UI running (`payment-gateway`) and the API with no ready pods (`payment-gateway-api` at `0/0`).

---

## 2) Start port-forward to the UI

In a **separate terminal**, keep this running for the whole session:

```bash
kubectl port-forward svc/payment-gateway -n payment 8089:80 --address 0.0.0.0
```

**What it does:** Maps `localhost:8089` on your machine to the UI Service inside the cluster so students can use the browser without extra ingress setup.

---

## 3) Smoke-check the broken state (instructor only)

Open `http://localhost:8089` in the browser.

1. Confirm the AirPay UI **loads** (frontend is up).
2. Submit a test payment and confirm it **fails** (backend is down).

You are verifying the scenario is ready — do not show this check as step one of the demo. Demo 1 starts cold with `kubectl get namespaces`.

---

## 4) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Orient & reproduce the failure  
- `2_guide.md` — Investigate the namespace  
- `3_guide.md` — Ownership wall, fix, validate  

---

## Reset for another run (optional)

After Demo 3, if you scaled the API up or added labels, restore the broken baseline:

```bash
kubectl scale deployment payment-gateway-api -n payment --replicas=0
kubectl label deployment payment-gateway-api -n payment owner- cost-center- --overwrite 2>/dev/null || true
```

**What it does:** Scales the API back to 0 and removes manual `owner` / `cost-center` labels so the next session starts in the same broken state.

To redeploy cleanly from manifests:

```bash
kubectl apply -k sections/02a-payment-gateway-down/manifests/
```

**What it does:** Re-applies manifest state (including 0 API replicas and original labels).
