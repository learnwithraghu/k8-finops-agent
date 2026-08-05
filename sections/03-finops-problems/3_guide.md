# Demo 3: Finding Labels in Two Namespaces

**Time Budget:** 3-4 mins

> **Try it first:** Open the SkyLine Air cluster and keep an eye on label differences between namespaces.

### 1) Show the namespaces first
```bash
kubectl get namespaces
```
> *Talking point: We are going to compare the same kind of resources in two different namespaces.*

### 2) Check labels in the inventory namespace
```bash
kubectl get deployments -n inventory --show-labels
kubectl get services -n inventory --show-labels
```
> *Talking point: Note the label keys and values you see here.*

### 3) Check labels in the payment namespace
```bash
kubectl get deployments -n payment --show-labels
kubectl get services -n payment --show-labels
```
> *Talking point: Compare the labels with inventory — same kind of resources, different label patterns.*

### 4) Spot the inconsistency
```bash
kubectl describe deployment inventory-service -n inventory
kubectl describe deployment payment-processor -n payment
```
> *Talking point: The issue is not just missing labels; it is that labels vary by namespace, which makes manual review messy.*

