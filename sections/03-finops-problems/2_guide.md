# Demo 2: Locating Orphaned Assets

**Time Budget:** 2-3 mins

### 1) Inspect analytics in the default namespace
```bash
kubectl get deployment analytics-collector -n default -o yaml
```
> *Talking point: No namespace isolation, no ownership labels.*

### 2) Scan PVCs for orphans
```bash
kubectl get pvc -A
```
> *Talking point: Look for claims that seem disconnected or lack proper tagging.*

### 3) Scan ConfigMaps for missing labels
```bash
kubectl get configmaps -A --show-labels
```
