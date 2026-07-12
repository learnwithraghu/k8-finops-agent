# Slide Presentation Guide: Section 08 — From Findings to Actionable Tickets

## Video-to-slide mapping

| Video | Slide file | Notes |
|-------|------------|-------|
| **V1** — Issue tracker landscape | `slide1_tracker_landscape.svg` | Jira, Linear, GitHub Issues, custom tracker comparison |
| **V3** — Tracker backend walkthrough | `slide2_tracker_architecture.svg` | FastAPI internals, REST + MCP, IssueCreate fields |
| **V4** — Integration whiteboard | `slide4_integration_whiteboard.svg` | One agent, two MCP servers (K8s + tracker) |
| **V6** — Closed-loop pipeline | `slide5_closed_loop_pipeline.svg` | Full S05–S10 architecture update |

Videos V2 and V5 are live demos — no dedicated slides. Use the running board UI and agent code in the editor.

## Demo checkpoints

### V2 — Launch tracker (`1_guide.md`)
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```
Open `http://localhost:8085` — empty Kanban board.

### V3 — API walkthrough (`2_guide.md`)
Tour `service/app/main.py`, `models.py`, `mcp_server.py`. Manual curl to `/create-issue`.

### V5 — Agent demo (`3_guide.md`)
```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```
Verify tickets on `http://localhost:8085`.

## Instructor tips

- V1 sets context before any code — learners should understand *why* trackers matter
- V4 whiteboard is the conceptual bridge between tracker service and agent code
- V6 closes the section and previews Sections 09 (refactor) and 10 (Helm)
- Keep the tracker container running across V2–V5 demos
