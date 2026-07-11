# Demo 3: Verify the Baseline

**Time Budget:** 3 mins

**Narrative:** Before we deploy anything, let's confirm what the cluster looks like with nothing in it. This is your blank canvas — everything from Section 02 onwards builds on top.

---

### 1) Check for any existing workloads

```bash
kubectl get all -A
```

**What it does:** Lists every pod, service, deployment, and replicaset across all namespaces. In a clean cluster you should only see system components under `kube-system`.

> *Talking point: "If you see anything under the airline namespaces, something leaked from a previous run. That is what the cleanup script in the prereq guide prevents."*

---

### 2) Check services across namespaces

```bash
kubectl get svc -A
```

**What it does:** Lists all Services cluster-wide. The airline namespaces should be empty — only `kubernetes` in the `default` namespace and `kube-dns` in `kube-system`.

> *Expected: Two services total — `kubernetes` and `kube-dns`. Nothing in the airline namespaces.*

---

### 3) Check node details

```bash
kubectl get nodes -o wide
```

**What it does:** Shows node info including OS, kernel version, container runtime, and internal IP. Useful for confirming the Kind node is healthy.

> *Talking point: "This single node runs everything. In production you would have many nodes — but the kubectl commands are the same."*

---

### 4) Confirm no workloads in airline namespaces

```bash
kubectl get pods -n booking-api
kubectl get pods -n payment
```

**What it does:** Explicitly checks two airline namespaces for pods. Both should return "No resources found."

> *Expected: Empty — no pods, no deployments, nothing. The namespaces are clean containers waiting for Section 02.*

---

**Next:** Foundation done. Next section deploys the airline app → `sections/02-airline-app-deployment`
