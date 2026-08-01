# Slide Presentation Guide: Section 08 — From Findings to Actionable Tickets

## Video-to-slide mapping

| Video | Slide file | Notes |
|-------|------------|-------|
| **V1** — Issue tracker landscape | `slide1_tracker_landscape.svg` | Jira, Linear, GitHub Issues, custom tracker comparison |
| **V3c** — Tracker backend walkthrough | `slide2_tracker_architecture.svg` | FastAPI internals, REST + MCP, IssueCreate fields |
| **V4** — Integration whiteboard | `slide4_integration_whiteboard.svg` | One agent, two MCP servers (K8s + tracker) |
| **V6** — Closed-loop pipeline | `slide5_closed_loop_pipeline.svg` | Full S05–S10 architecture update |

Videos V2, V3a, V3b, V5, and V5b are live demos — no dedicated slides. Use the running board UI and agent code in the editor.

## Demo checkpoints

### V2 — Launch tracker (`1_guide.md`)
Keep **Terminal 1** (K8s MCP) and **Terminal 2** (tracker) running from `0_prerequisite_guide.md`.
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```
Open `http://localhost:8085` — empty Kanban board.

### V3a — LLM lists tracker tools (`2_guide.md`)
```bash
python3 sections/08-from-findings-to-tickets/agent/prompt_list_tracker_tools.py
```
Expected: LLM names `create_issue`, `list_issues`, `get_issue`, `update_issue`. No tickets created.

### V3b — Code walkthrough (`3_guide.md`)
Compare Section 07 `mcp_client.py` / `structured_auditor.py` with Section 08 `mcp_client.py` / `tracker_auditor.py`.

### V3c — API walkthrough (`4_guide.md`)
Tour `service/app/main.py`, `models.py`, `mcp_server.py`. Manual curl to `/create-issue`.

### V5 — Agent demo (`5_guide.md`)
```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```
Verify three `payment` tickets on `http://localhost:8085`.

### V5b — Widen prompt (`6_guide.md`)
Manually change the collect line in `tracker_auditor.py` to:
```text
- kubectl_get resourceType=deployments allNamespaces=true output=json
```
Re-run the agent and confirm tickets for other namespaces.

## Instructor tips

- V1 sets context before any code — learners should understand *why* trackers matter
- Keep **two** MCP terminals running across V2–V5b demos (K8s + tracker)
- V3a is the smallest LLM proof before the full agent
- V3b is the delta talk — what is new vs Section 07
- V4 whiteboard is the conceptual bridge between tracker service and agent code
- V5 scopes to `payment` for reliability; V5b is the one-line widen
- V6 closes the section and previews Sections 09 (observability) and later packaging
