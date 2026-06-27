# Demo 1: Environment Cleanup & Tool Verification

**Time Budget:** 2-3 mins

### 1) Clean old state
```bash
./helper/cleanup.sh
```
> *Expected: Removes any old Kind clusters.*

### 2) Verify Docker is installed and running
```bash
docker --version
docker info
```

### 3) Verify Helm is installed
```bash
helm version --short
```

### 4) Verify Kind is installed
```bash
kind version
```

### 5) Verify kubectl is installed
```bash
kubectl version --client
```
