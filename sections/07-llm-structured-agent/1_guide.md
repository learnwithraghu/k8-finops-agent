# Demo 1: Providing Snapshot and Rules to LLM

**Time Budget:** 3-4 mins

### 1) Install dependencies
```bash
python3 -m pip install -r sections/07-llm-structured-agent/requirements.txt
```

### 2) Inspect the rules and skeleton code
```bash
cat sections/07-llm-structured-agent/config/tagging-rules.yaml
cat sections/07-llm-structured-agent/agent/analyser.py
cat sections/07-llm-structured-agent/agent/models.py
cat sections/07-llm-structured-agent/agent/main.py
```
> *Talking point: We feed the unstructured snapshot + tagging rules to the LLM to get structured findings based on models.py schemas.*

### 3) Run the structured agent
*(Assuming the Section 06 snapshot is at `/tmp/section06-snapshot.json`)*
```bash
PYTHONPATH=sections/07-llm-structured-agent \
  python3 -m agent.main --snapshot /tmp/section06-snapshot.json
```
