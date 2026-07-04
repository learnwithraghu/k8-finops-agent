# Instructor Prerequisite: Cluster & Manifest Check

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through manifest discovery during the live demo.

**Time Budget:** 1–2 mins

---

## Before you start

Confirm Section 01 is complete:

- Kind cluster `finops-cluster` is running
- kubectl works against the cluster
- Airline namespaces exist (`booking-api`, `flight-search`, `inventory`, `payment`, `airline`)

Quick check:

```bash
kubectl cluster-info
kubectl get namespaces
```

**What it does:** Verifies cluster connectivity and that the five airline namespaces are present.

---

## 1) Inspect the manifest layout

```bash
ls sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```

**What it does:** Shows the service directories that Kustomize will deploy — one per airline service plus a `problem-resources` directory.

---

## 2) Inspect the Kustomize file

```bash
cat sections/02-airline-app-deployment/manifests/airline-k8-deployment/kustomization.yaml
```

**What it does:** Shows which resources Kustomize will apply. This is the entry point for `kubectl apply -k`.

> *Talking point: "Kustomize lets you compose manifests without templating. One file controls the whole deployment."*

---

## 3) Ready to teach

When checks pass, start the live walkthrough with:

- `1_guide.md` — Deploy and validate the app
- `2_guide.md` — Workload deep dive

## Reset for another run (optional)

To redeploy cleanly:

```bash
kubectl delete -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/ 2>/dev/null || true
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```

**What it does:** Tears down and reapplies all resources so the demo starts fresh.
