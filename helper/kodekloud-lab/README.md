# KodeKloud Lab - Python Setup Guide

This guide explains how to install Python and set up the local agent dependencies in a KodeKloud playground or a container running Alpine Linux.

## Installation & Environment Setup

Run the following command to update packages, install Python 3 and pip, create a virtual environment, activate it, and install the required packages for the local Python agent:

```bash
apk update && apk add python3 py3-pip && python3 -m venv venv && source venv/bin/activate && pip install -r sections/04-local-python-agent/requirements.txt
```

### What this does:
1. **`apk update`**: Updates the package index in the Alpine container.
2. **`apk add python3 py3-pip`**: Installs Python 3 and its package manager (`pip`).
3. **`python3 -m venv venv`**: Creates a new Python virtual environment in the `venv` directory.
4. **`source venv/bin/activate`**: Activates the virtual environment.
5. **`pip install -r ...`**: Installs the required FinOps agent libraries (such as Kubernetes and PyYAML).
