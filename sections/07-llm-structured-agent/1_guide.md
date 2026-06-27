# Demo 1: Providing Snapshot and Rules to LLM

**Time Budget:** 3-4 mins

> *Note: Ensure your `supergateway` from Section 05 is still running in the background!*

### 1) Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r sections/07-llm-structured-agent/requirements.txt
```

### 2) Inspect the code
```bash
cat sections/07-llm-structured-agent/agent.py
```
> *Talking point: We took the data collection logic from Section 06 and added LangChain/OpenAI analysis on top to get structured findings.*

### 3) Run the structured agent
```bash
python3 sections/07-llm-structured-agent/agent.py
```
