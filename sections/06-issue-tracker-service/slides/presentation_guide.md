# Slide Presentation Guide: Section 06 Issue Tracker Service

This guide accompanies the generated SVG slide assets to help you narrate this section before jumping into the live demo.

---

## Slide 1: Issue Tracker Overview
*   **File**: [slide1_overview.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide1_overview.svg)
*   **Narrative Focus**:
    *   Explain the problem: When an LLM scanner runs, it outputs raw insights. But in the real world, developers and DevOps teams don't look at log files; they use ticketing systems (like Jira, ServiceNow, or GitHub Issues) to track work.
    *   Introduce the solution: A simple Kanban board issue tracker service that exposes a REST API. This allows the AI agent to write directly to a structured board, bridging the gap between automation and human execution.
    *   Highlight: We need programmatic creation, interactive boards, and clear accountability.

---

## Slide 2: Service Architecture
*   **File**: [slide2_architecture.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide2_architecture.svg)
*   **Narrative Focus**:
    *   How the components interact: Explain that the service is written in **FastAPI** and is self-contained.
    *   Inside the Docker container: The service listens on container port `8000` (mapped to host port `8085`). It handles API routing, serves static UI files (HTML/CSS/JS board UI), and writes issues to an **In-Memory Store** (`app/store.py`).
    *   Emphasize: Because the store is in-memory, restarting the container resets the board. This keeps our local testing clean and stateless.

---

## Slide 3: API Contract & JSON Payload
*   **File**: [slide3_payload_schema.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide3_payload_schema.svg)
*   **Narrative Focus**:
    *   Explain the API Contract: Dive into the fields that our Python Agent will need to send to `POST /create-issue`.
    *   **Kubernetes Context**: `namespace`, `resource_name`, and `resource_kind` pin the issue down to the exact cluster object that violated rules.
    *   **Impact & Priority**: `cost_impact` (floating dollar amount of waste per month) and `priority` (critical, high, medium, low) allow teams to sort findings by ROI.
    *   **Ownership**: `suggested_owner` and `suggested_cost_center` help automatically route issues to the correct squad rather than general backlog queues.

---

## Slide 4: [DEMO 01] Running & Exploring the Tracker
*   **File**: [slide4_demo1.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide4_demo1.svg)
*   **Narrative Focus**:
    *   This is a transitional slide indicating to the class that we are about to launch the container.
    *   **Demo Steps**:
        1. Open a terminal and run the Docker build command:
           ```bash
           docker build -t finops-issue-tracker:latest sections/06-issue-tracker-service/service
           ```
        2. Start the tracker container:
           ```bash
           docker run --rm -p 8085:8000 --name finops-issue-tracker finops-issue-tracker:latest
           ```
        3. Open a browser and visit:
           - Kanban Board UI: `http://localhost:8085` (show it's currently empty).
           - Swagger Documentation: `http://localhost:8085/docs` (briefly walk through `/create-issue` and `PATCH /issue/{id}`).

---

## Slide 5: Ticket Creation & Lifecycle
*   **File**: [slide5_flow_handoff.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide5_flow_handoff.svg)
*   **Narrative Focus**:
    *   Walk through the flow of a ticket's life:
        1. An API client sends a `POST /create-issue` request with the JSON payload.
        2. The backend generates a sequential integer `id`, creates a Jira-style key (e.g. `FINOPS-0001`), and sets the default status to `"backlog"`.
        3. The Kanban board receives the update and renders a card in the Backlog column, displaying cost impact, priority, and category.
    *   Explain how the user can interactively drag cards on the board, which triggers a `PATCH` request behind the scenes.

---

## Slide 6: [DEMO 02] API Ticket Creation & Board Lifecycle
*   **File**: [slide6_demo2.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide6_demo2.svg)
*   **Narrative Focus**:
    *   Transition to the second demo.
    *   **Demo Steps**:
        1. Open a new terminal and fire the `curl` POST request to create an unallocated resource ticket.
        2. Flip back to the browser window and show that the card `FINOPS-0001` immediately appears on the board.
        3. In the UI, click on the card to open its detail view, assign it to a team, and save.
        4. Drag the card across columns from `Backlog` → `To Do` → `In Progress` → `Done` to demonstrate lifecycle tracking.

---

## Slide 7: Summary & Next Steps
*   **File**: [slide7_summary.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/06-issue-tracker-service/slides/slide7_summary.svg)
*   **Narrative Focus**:
    *   Recap Section 06 achievements: We have a functioning Kanban board that represents our tracking destination.
    *   Preview Section 07: We will link our LangChain Python Agent directly to this API. Instead of manual curls, the agent will analyze the cluster live and raise tickets automatically.
