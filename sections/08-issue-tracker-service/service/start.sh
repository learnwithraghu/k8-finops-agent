#!/bin/bash
set -e

python -m app.mcp_server &
uvicorn app.main:app --host 0.0.0.0 --port 8000
