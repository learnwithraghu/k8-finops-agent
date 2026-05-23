# Section 09: Simple Agent Example

This section shows the simplest possible FinOps agent.
No classes, no dataclasses, just plain functions and a single YAML config.

## Files

- `config.yaml` – default settings (overridden by `.env`)
- `.env.example` – example environment variables
- `main.py` – loads config + `.env`, orchestrates the flow
- `k8_data.py` – fetches Kubernetes pod usage
- `bedrock_client.py` – sends data to AWS Bedrock
- `issue_tracker.py` – posts findings to the issue tracker

## How it works

1. `main.py` loads `config.yaml` and `.env` (`.env` values override YAML)
2. Calls `get_k8_data()` to fetch `kubectl top pods`
3. Sends the raw data to Bedrock via `analyze_with_bedrock()`
4. Parses the JSON array of findings from the LLM response
5. Calls `send_to_tracker()` to create one issue per finding

## Run it

```bash
cd sections/09-simple-agent-example
python main.py
```

## Prerequisites

- `kubectl` configured and pointing to your cluster
- AWS credentials available (env vars or ~/.aws/credentials)
- `python-dotenv` installed (`pip install python-dotenv`)
- Issue tracker running (see section 06)
