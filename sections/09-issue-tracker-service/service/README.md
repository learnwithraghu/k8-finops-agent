# Service

This folder contains the local issue tracker for Section 09.

## What it is
A simple Jira-style Kanban board built with FastAPI, HTML, CSS, and JavaScript.

## What it does
- creates tickets through `/create-issue`
- opens tickets through `/issue/{id}`
- updates assignment and status through `PATCH /issue/{id}`
- shows the API docs at `/docs` with payload guidance for `/create-issue`
- renders a board with backlog, to do, in progress, and done columns

## Files
- `app/main.py` — API and UI entrypoint
- `app/models.py` — request/response models
- `app/store.py` — local JSON storage
- `app/static/` — board UI
- `Dockerfile` — container image for local runs

## Run
Build the image from this folder and run it on host port 8085 (container port 8000).
