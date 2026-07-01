# Demo 2: Create Namespaces

**Time Budget:** 2 mins

**Narrative:** Real clusters separate workloads by namespace. We will create the ones our airline services live in — each namespace maps to a team or service boundary.

---

### 1) Create the baseline namespaces

```bash
kubectl create namespace booking-api
kubectl create namespace flight-search
kubectl create namespace inventory
kubectl create namespace payment
kubectl create namespace airline
```

**What it does:** Creates five namespaces — one per airline service. These are the boundaries Section 02 deploys into.

> *Talking point: "In production, namespaces are your first layer of isolation. They control RBAC, network policies, and resource quotas. Here we use them to keep services organized."*

---

### 2) Verify namespaces exist

```bash
kubectl get namespaces
```

**What it does:** Lists all namespaces. You should see the five new ones plus the Kubernetes defaults (`default`, `kube-system`, `kube-public`, `kube-node-lease`).

> *Expected: Nine namespaces total — five airline ones plus four system defaults.*

---

### 3) Confirm kubectl access works

```bash
kubectl auth can-i get pods -A
```

**What it does:** Checks whether your current user can list pods across all namespaces. A `yes` means your kubeconfig has the right permissions.

> *Talking point: "This is a quick RBAC sanity check. In managed clusters, developers often hit permission errors — this confirms you are admin locally."*

---

**Next:** Namespaces are ready. Next we verify the full baseline is clean → `3_guide.md`
