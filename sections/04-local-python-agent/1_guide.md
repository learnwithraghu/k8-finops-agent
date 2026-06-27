# Demo 1: Setup and Agent Configuration

**Time Budget:** 3-4 mins

### 1) Read the tagging rules and collector code
```bash
cat sections/04-local-python-agent/config/tagging-rules.yaml
cat sections/04-local-python-agent/agent/collect.py
```
> *Talking point: We aren't doing logic in the collector; it just dumps raw JSON.*

### 2) Setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r sections/04-local-python-agent/requirements.txt
```

### 3) Check cluster access
```bash
kubectl cluster-info
```
