# Demo 1: Containerization and Config Handling

**Time Budget:** 4-5 mins

### 1) Review Helm chart structure
```bash
tree sections/11-k8-native-agent/helm/
cat sections/11-k8-native-agent/helm/Chart.yaml
cat sections/11-k8-native-agent/helm/values.yaml
```

### 2) Preview Helm templates
```bash
helm template finops-agent sections/11-k8-native-agent/helm/
```
> *Talking point: We use Helm to manage config, rules, and secrets natively in K8s.*

### 3) Build the Docker image
```bash
cd sections/11-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
```

### 4) Load image into Kind cluster
```bash
# Find your cluster name with: kind get clusters
kind load docker-image finops-agent:latest --name finops-cluster
```
