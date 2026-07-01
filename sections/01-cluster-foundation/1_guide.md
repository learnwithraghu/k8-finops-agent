# Demo 1: Create the Kind Cluster

**Time Budget:** 2 mins

**Narrative:** We need a local Kubernetes cluster. Kind runs one inside Docker — fast, disposable, no cloud account needed. This is how most people prototype K8 workflows on their laptop.

---

### 1) Create the cluster

```bash
kind create cluster --name finops-cluster
```

**What it does:** Spins up a single-node Kubernetes cluster inside a Docker container. Takes about 30 seconds on a good machine.

> *Talking point: "Kind stands for 'Kubernetes IN Docker.' It gives you a real API server, real etcd, real kubelet — just running in containers instead of VMs. Perfect for local dev and teaching."*

---

### 2) Confirm the cluster exists

```bash
kind get clusters
```

**What it does:** Lists all Kind clusters on your machine. You should see `finops-cluster`.

---

### 3) Confirm kubectl can talk to it

```bash
kubectl cluster-info
```

**What it does:** Hits the Kubernetes API server and prints its URL. If this works, kubectl is wired correctly to the new cluster.

> *Talking point: "Kind automatically updates your kubeconfig. That is why kubectl works immediately — no manual config step."*

---

### 4) Confirm nodes are ready

```bash
kubectl get nodes
```

**What it does:** Lists all cluster nodes and their status. You should see one node in `Ready` state.

> *Expected: One node listed, status `Ready`, role `control-plane`.*

---

**Next:** Cluster is up. Next we create the namespaces our airline app will use → `2_guide.md`
