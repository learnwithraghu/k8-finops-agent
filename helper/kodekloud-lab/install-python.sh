#!/bin/bash
# helper/kodekloud-lab/install-python.sh
# ─────────────────────────────────────────────────────────────────────────────
# Installs Python 3 and pip (Alpine), creates a virtual environment, activates
# it, and installs dependencies for sections 04 and 05.
#
# Run from the repo root:
#   bash helper/kodekloud-lab/install-python.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() { echo -e "\n${BLUE}================================${NC}\n${BLUE}$1${NC}\n${BLUE}================================${NC}"; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_info()    { echo -e "${YELLOW}→ $1${NC}"; }

# Resolve repo root regardless of where the script is invoked from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

print_header "Python Environment Setup"

# ── Step 1: Install Python (Alpine) ──────────────────────────────────────────
if command -v apk > /dev/null 2>&1; then
    print_info "Alpine detected — installing python3 and py3-pip..."
    apk update
    apk add python3 py3-pip
    print_success "Python 3 and pip installed"
else
    print_info "Non-Alpine OS detected — assuming python3 is already installed"
    python3 --version || { echo "python3 not found. Please install it first."; exit 1; }
fi

# ── Step 2: Create virtual environment ───────────────────────────────────────
print_info "Creating virtual environment at ${REPO_ROOT}/.venv ..."
python3 -m venv "${REPO_ROOT}/.venv"
print_success "Virtual environment created"

# ── Step 3: Activate and install dependencies ─────────────────────────────────
print_info "Activating virtual environment..."
# shellcheck disable=SC1091
source "${REPO_ROOT}/.venv/bin/activate"
print_success "Virtual environment activated"

print_info "Installing repo dependencies..."
pip install -r "${REPO_ROOT}/requirements.txt"
print_success "Dependencies installed"

print_header "Python Setup Complete!"
echo -e "${GREEN}Virtual environment is active. Run your agents with:${NC}"
echo ""
echo "  # Section 06 (prompt -> MCP -> plain-English answer)"
echo "  python3 sections/06-mcp-data-agent/query_agent.py"
echo ""
echo "  # Section 06 (MCP -> label audit via agent)"
echo "  python3 sections/06-mcp-data-agent/code/label_auditor.py"
echo ""
echo -e "${YELLOW}Note: re-activate the venv in new shells with:${NC}"
echo "  source .venv/bin/activate"
echo ""
