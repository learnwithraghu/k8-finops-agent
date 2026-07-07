# Demo 2: Label Inconsistencies Deep Dive

**Time Budget:** 2–3 mins

**Narrative:** In Kubernetes, labels are the glue that connects resources together. When services fail to discover pods, or deployments fail to match replica sets, the culprit is often a mismatched label. Let's practice inspecting configs to find label inconsistencies.

---

### 1) Open the Deployment Configuration

Let's start by looking at a deployment configuration to see what labels are defined. 

```bash
cat manifests/airline-k8-deployment/flight-search-service/deployment.yaml
```

**What to look for:** Notice the `spec.selector.matchLabels` and compare them with the labels under `spec.template.metadata.labels`. These must match perfectly for the Deployment to manage its Pods. 

> *Talking point: "A common mistake during copy-pasting is changing the template labels but forgetting to update the selector labels. This leads to orphan pods."*

---

### 2) Check the Service Configuration

Next, open the service config that is supposed to route traffic to these pods.

```bash
cat manifests/airline-k8-deployment/flight-search-service/service.yaml
```

**What to look for:** Look at the `spec.selector` in the Service. The Service uses these labels to find the target pods.

> *Talking point: "If the Service selector says `app: flight-search`, but the Pod template has `app: flight-search-svc`, the service won't route traffic to any pods. The endpoints list will be empty."*

---

### 3) Spotting the Inconsistency

Let's compare them side-by-side using `kubectl` if they are already deployed:

```bash
# Check the labels on the running pods
kubectl get pods -n flight-search --show-labels

# Check the selector on the service
kubectl describe svc flight-search-service -n flight-search | grep Selector
```

**What it does:** By slowly comparing the output of these two commands, you can often spot subtle typos (like `version: v1` vs `version: v1.0`) or missing labels that break the connection.

> *Expected: You should identify if the selector labels perfectly match the labels attached to the pods.*

---

**Try it:** Open your `manifests/airline-k8-deployment/` configs in the editor. Deliberately change a label in `flight-search-service/service.yaml`, deploy it, and watch how the endpoints disappear. Then fix it and watch them recover.

**Next:** Now that you know how to trace label inconsistencies, let's look at more complex failures. Next section simulates a payment failure → `sections/02a-payment-gateway-down`
