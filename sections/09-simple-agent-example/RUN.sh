#!/bin/bash
# Quick start: Run the Simple Agent from repo root
#
# IMPORTANT: Before running this script, configure your AWS credentials locally:
#   Option 1: aws configure
#   Option 2: export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... in your shell
#   Option 3: Set them in ~/.aws/credentials
#
# DO NOT put AWS credentials in .env or any file - that's a security risk!
# See sections/09-simple-agent-example/guide.md for full setup instructions.

# Make sure you're in the repo root
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || cd /Users/raghunandanask/Desktop/github-repo/k8-finops-agent

# Activate the root virtual environment
source venv/bin/activate

# Run the agent
PYTHONPATH=sections/09-simple-agent-example python -m main
