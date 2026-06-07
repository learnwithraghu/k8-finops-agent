# The K8s Mystery: Who Owns the Broken Service?

## Game Design Document

### Overview
An interactive narrative-driven simulation where the player experiences the real-world pain of operating a large Kubernetes cluster without proper FinOps practices — specifically around ownership, labeling, and cost attribution.

### Target Audience
- Platform engineers
- SREs / DevOps engineers
- Engineering managers
- Anyone learning about FinOps and cloud cost management

### Learning Objectives
After completing this game, players should understand:
1. Why proper labeling and ownership tagging is critical for operational efficiency
2. The true cost of "unowned" resources in terms of MTTR, revenue, and team morale
3. How FinOps practices directly impact incident response and system reliability
4. The compound effect of poor resource attribution during critical incidents

---

## Game Structure: 4 Acts

### Act 1: The Incident Begins (Build Tension)
**Scene 1.1 — The 2 AM Page**
- Player receives a realistic PagerDuty-style critical alert
- Visual: Animated alert banner, dark mode UI
- Audio: Optional alert sound (can be muted)
- Interaction: Player must acknowledge the alert to proceed

**Scene 1.2 — The Dashboard**
- Show a Grafana-style dashboard with cascading red alerts
- Visual: Interactive charts showing failure propagation
- Key metric: "payment-api" service returning 500s
- Interaction: Player clicks through to investigate

**Scene 1.3 — First Attempt: Check Labels**
- Player tries to find service ownership via Kubernetes labels
- Visual: K8s resource cards (Pods, Services, Deployments)
- The Pain: Labels are missing, inconsistent, or wrong
  - `owner=unknown`, `owner=tbd`, `cost-center=legacy`
  - Namespace `team-a-prod` has services owned by `team-b`
  - Some resources have NO labels at all
  - Annotations point to engineers who left months ago

### Act 2: The Investigation Deepens (Frustration Builds)
**Scene 2.1 — Slack Chaos**
- Player must "ping" different Slack channels to find the owner
- Interaction: Click buttons to message different teams
- Result: Most teams say "not ours" or "we handed that off"

**Scene 2.2 — The Org Chart Hunt**
- Navigate a broken organizational chart
- Visual: Interactive org chart with restructuring history
- The Pain: Teams have been reorganized 3 times; no clear ownership

**Scene 2.3 — The Cost Report Dead End**
- Check cloud cost dashboards for clues
- Visual: AWS Cost Explorer-style charts
- The Pain: 60% of resources are "untagged" or "unallocated"
- Show $50K/month in mystery spend

**Scene 2.4 — Escalation Roulette**
- Keep escalating up the chain
- Visual: Animation of messages bouncing around
- The Pain: Every escalation adds 30+ minutes; no one knows

**Visual Metaphor**: A maze/fog-of-war that gets darker the longer the player takes.
Timer shows: "Downtime: 45 minutes... Revenue lost: $XX,XXX"

### Act 3: The Revelation (The "Aha!" Moment)
**Scene 3.1 — Accidental Discovery**
- Player finally finds the owner by accident in a random thread
- Revelation: "payment-api was migrated to team-payments last quarter but nobody updated the labels"

**Scene 3.2 — The Consequence Screen**
Show the full impact:
- Revenue lost: $127,000
- MTTR: 4 hours 23 minutes
- Customer tickets: 340
- SLO breach: 99.9% → 94.2%
- On-call engineer burnout level: MAXIMUM

### Act 4: The FinOps Solution (Relief & Learning)
**Scene 4.1 — The Rewind**
- Game rewinds to the same incident
- Visual: Time-rewind animation

**Scene 4.2 — With Proper FinOps**
Show the same scenario with FinOps practices:
- Hover over any pod → instant owner, cost center, team Slack
- Click service → auto-linked to Service Catalog
- Real-time cost per service, per team, per environment
- Automated tagging policies preventing drift

**Scene 4.3 — Side-by-Side Comparison**
| Metric | Without FinOps | With FinOps |
|--------|---------------|-------------|
| Time to identify owner | 4+ hours | 30 seconds |
| Revenue impact | $127,000 | $0 |
| Teams disrupted | 8+ | 1 (the actual owner) |
| Customer impact | 340 tickets | 0 |

**Scene 4.4 — Interactive FinOps Dashboard**
- Beautiful single pane of glass
- Ownership + Cost + Health, all linked
- Player can explore and interact

---

## Mini-Games & Interactive Elements

### 1. "Label Detective"
- Show a pod manifest with missing/broken labels
- Player drags correct labels from a "FinOps Policy" sidebar
- Wrong labels = error messages
- Right labels = green check + educational explanation

### 2. "Cost Allocation Puzzle"
- Show $100K cloud bill with 60% "untagged"
- Player drags resources into correct team buckets
- Watch the bill "light up" as attribution improves

### 3. "The Escalation Ladder"
- Click through an org chart to find the right owner
- Without FinOps: 8 clicks, dead ends
- With FinOps: 1 click, instant answer

### 4. "MTTR Timer Challenge"
- Race against the clock to resolve the incident
- Each wrong guess adds 30 minutes
- Leaderboard: "Can you beat the FinOps-enabled time?"

---

## Visual Design System

### Color Coding
- 🔴 Red: Untagged/unowned resources, errors, critical alerts
- 🟡 Yellow: Partially tagged, warnings, "almost there" traps
- 🟢 Green: Properly tagged, success, FinOps-enabled
- 🔵 Blue: Informational, clickable elements
- ⚫ Dark: Background (on-call night shift aesthetic)

### Icons (Material Symbols via Streamlit)
- Pods: `:material/deployed_code:`
- Services: `:material/cloud:`
- Alerts: `:material/warning:` / `:material/error:`
- Teams: `:material/groups:`
- Cost: `:material/paid:` / `:material/account_balance:`
- Time: `:material/schedule:` / `:material/timer:`
- Success: `:material/check_circle:`
- Failure: `:material/cancel:`

### Typography
- Headings: Large, bold, with emoji/icon accents
- Body: Readable, with clear hierarchy
- Metrics: Monospace for numbers (MTTR, costs)

---

## Technical Architecture

### File Structure
```
visuals/k8s_finops_mystery/
├── app.py                    # Main entry point
├── components/
│   ├── __init__.py
│   ├── act1_incident.py      # Act 1 scenes
│   ├── act2_investigation.py # Act 2 scenes
│   ├── act3_revelation.py    # Act 3 scenes
│   ├── act4_solution.py      # Act 4 scenes
│   ├── minigames.py          # Mini-game components
│   └── state_manager.py      # Session state helpers
├── assets/
│   ├── icons/                # Custom SVG/PNG icons
│   └── images/               # Background images, diagrams
└── utils/
    ├── __init__.py
    └── data_generators.py    # Mock K8s data, cost data
```

### State Management
- Use `st.session_state` for:
  - Current act/scene
  - Player choices and progress
  - Timer and score
  - Mini-game completion status

### Key Streamlit Features Used
- `st.set_page_config`: Dark theme, page title
- `st.columns`: Layout for side-by-side comparisons
- `st.metric`: Real-time metrics (MTTR, costs)
- `st.progress`: Timer and completion indicators
- `st.button`: Interactive choices
- `st.error` / `st.warning` / `st.success`: Alert banners
- `st.plotly_chart`: Cost charts, dashboards
- `st.graphviz_chart`: Org charts, K8s topology
- `st.markdown`: Rich text with HTML/CSS styling
- `st.session_state`: Game state persistence

---

## Future Enhancements
- [ ] Multiplayer leaderboard
- [ ] Additional scenarios (database incident, security breach)
- [ ] Integration with real K8s APIs for live demos
- [ ] Exportable "FinOps readiness scorecard"
- [ ] Voice narration for accessibility

---

## Success Metrics
- Player completes all 4 acts
- Player demonstrates understanding via mini-games
- Post-game survey: "Would you advocate for FinOps practices?"
