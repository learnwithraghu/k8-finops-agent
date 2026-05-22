# K8s FinOps Agent - Skill for Updating Usage Guide

## Purpose

This skill ensures the `USAGE.md` guide stays up-to-date whenever code changes are made to the agent.

## When to Use

Use this skill when:
- Adding new CLI arguments or flags
- Changing environment variables
- Adding new configuration options
- Modifying the execution flow
- Adding new features that affect usage

## Workflow

### Step 1: Identify Changes

After making code changes, review what affects user-facing behavior:
- New command-line arguments
- New environment variables
- Changed default values
- New configuration files
- New execution modes

### Step 2: Update USAGE.md

Update the following sections as needed:

#### Section: Step 2 - Environment Variables
Update if new env vars are added:
```markdown
**Required variables in `.env`:**
```bash
# Existing vars...
NEW_VAR=default_value  # <-- Add new vars here
```
```

#### Section: Step 6 - Run Options
Add new run options:
```markdown
### Option D: New Feature

```bash
# Description of new feature
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  --env-file .env \
  k8-finops-agent:latest \
  --new-flag
```
```

#### Section: Advanced Usage
Add new advanced options:
```markdown
### New Advanced Feature

```bash
# Description
command --new-option
```
```

#### Section: Troubleshooting
Add common issues:
```markdown
### Issue: New Error Message
```bash
# Solution steps
```
```

### Step 3: Validate Guide

Ensure all examples in USAGE.md:
- Use correct file paths
- Reference existing files
- Match actual CLI arguments
- Have working commands

### Step 4: Update File Structure

If new directories/files are added, update:
```markdown
## File Structure Reference

```
k8-finops-agent/
├── new-directory/      # <-- Add new entries
│   └── new-file.yaml
```
```

## Checklist

When updating USAGE.md, verify:

- [ ] All CLI arguments match `agent/main.py`
- [ ] All environment variables match `.env.example`
- [ ] All file paths exist in the repo
- [ ] Docker commands use correct image name
- [ ] Kind cluster name matches (`finops-cluster`)
- [ ] Example outputs match actual behavior
- [ ] Troubleshooting covers common errors
- [ ] File structure section is accurate

## Quick Reference

### CLI Arguments (from main.py)
```python
parser.add_argument('--kubeconfig', ...)
parser.add_argument('--namespace', '-n', ...)
parser.add_argument('--dry-run', '-d', ...)
parser.add_argument('--mock', '-m', ...)
parser.add_argument('--mock-github', ...)
parser.add_argument('--threshold', '-t', ...)
parser.add_argument('--log-level', '-l', ...)
```

### Environment Variables (from .env.example)
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `GITHUB_TOKEN`
- `GITHUB_REPO`
- `INSTANCE_TYPE`
- `KUBECONFIG_PATH`
- `TARGET_NAMESPACE`
- `LOG_LEVEL`
- `DRY_RUN`
- `MIN_COST_THRESHOLD`
- `BEDROCK_MODEL_ID`
- `BEDROCK_MAX_TOKENS`
- `BEDROCK_TEMPERATURE`
- `USE_MOCK`
- `USE_MOCK_GITHUB`

### Key Files to Reference
- `agent/main.py` - CLI arguments and entry point
- `.env.example` - Environment variables
- `Dockerfile` - Build instructions
- `config/` - Configuration files

## Automation

Consider adding a CI check that:
1. Parses CLI arguments from `agent/main.py`
2. Compares with USAGE.md examples
3. Fails build if USAGE.md is outdated

Example script:
```python
#!/usr/bin/env python3
"""Validate USAGE.md is up-to-date."""

import re
import sys
from pathlib import Path

# Parse CLI args from main.py
main_py = Path('agent/main.py').read_text()
args = re.findall(r"parser.add_argument\('([^']+)'", main_py)

# Parse args from USAGE.md
usage_md = Path('USAGE.md').read_text()
usage_args = re.findall(r'--[\w-]+', usage_md)

# Check for missing args
missing = set(args) - set(usage_args)
if missing:
    print(f"USAGE.md missing args: {missing}")
    sys.exit(1)

print("USAGE.md is up-to-date")
```
