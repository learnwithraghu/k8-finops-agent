# Video: Tagging Rules at a Glance (SkyLine Air)

**Time Budget:** 2 min
**Format:** Talking head + scroll through `examples/tagging-rules.yaml`
**Prerequisites:** `0_tagging_yaml_guide.md`

---

## Transcript

### Opening

Welcome back. You know *why* we use YAML for tagging policy. Now let us look at *what is inside* `tagging-rules.yaml` — at a high level, without drowning in every line. Think of this file as SkyLine Air's **governance dictionary**: the words the whole organization agrees on when labeling Kubernetes resources.

Keep the file open as we go. We are not memorizing it — we are building a map.

---

### The keys that matter

**`required_tags`** — the non-negotiables. Every workload we care about should carry at least `owner`, `environment`, `cost-center`, `application`, and `tier`. If any of these are missing, FinOps cannot allocate cost or route a finding to the right team. This is the shortest section in the file and the most important one.

**`label_mappings`** — the real-world escape hatch. Teams rarely label things with one consistent key. Someone uses `env`, someone uses `app.kubernetes.io/env`. This section says: *if you see any of these keys, count it as satisfying the rule.* That is how you govern a messy cluster without forcing a big-bang relabeling project on day one.

**`cost_centers`** — SkyLine Air's org chart in tag form. Booking engine, payment, inventory, customer service, analytics, platform. When a pod burns CPU, finance wants to know *which business unit* pays for it. These values mirror how SkyLine Air thinks about money — not generic cloud labels.

**`environments`**, **`tiers`**, and **`compliance_levels`** — the vocabulary for *where* and *how critical* a workload is. Dev versus prod. Frontend versus database. PCI-DSS for payment flows versus standard for internal tools. You do not need every compliance nuance today — just know these lists define what *valid* values look like when we audit.

**`resource_types`** and **`excluded_namespaces`** — scope. We scan Deployments, Services, PVCs, and a few other objects that actually carry cost or ownership risk. We skip `kube-system` and friends because flagging system components as "untagged" would just create noise.

---

### Relating this to your organization

SkyLine Air is our teaching story — airline booking, payments, inventory. Your company will have different cost centers and compliance labels. That is fine. The **shape** of this file is what transfers: required tags, alias mappings, allowed values, and scan boundaries. Swap the lists for your org; keep the structure.

If you are a platform engineer, this is the file you socialize with team leads before anyone writes an agent. If you are on an application team, it tells you exactly what labels your next deployment should carry.

---

### Close

You now have the policy and the vocabulary. Next we leave the whiteboard and go into the cluster — we will read these rules, then inspect real SkyLine Air workloads and see where tags are missing, inconsistent, or simply never applied. That is where the FinOps pain becomes visible — and where our agent story begins.

---

## Key takeaways

- `required_tags` defines the minimum metadata every governed resource needs
- `label_mappings` handles inconsistent labeling without blocking progress
- `cost_centers`, `environments`, `tiers`, and `compliance_levels` encode org-specific allowed values
- `resource_types` and `excluded_namespaces` keep audits focused on meaningful objects

## Demo handoff

Next → `1_guide.md` — identify untagged resources in the live cluster
