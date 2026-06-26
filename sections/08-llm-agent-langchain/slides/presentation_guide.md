# Section 08: LLM Decision Flow — Slide Guide & Narrative

This guide provides the slide-by-slide narration scripts and live demo handoff instructions for **Section 08: LLM Decision Flow**.

> **Design System**: High-tech Light canvas (#FFFFFF background with subtle dot grid pattern), rounded cards (rx="12" or rx="16"), high-contrast accents (Teal Trust #028090, Success Emerald #10B981, Warning Amber #D97706, Rose Red #EF4444), inline Lucide icons, `viewBox="0 0 1280 720"` (16:9), and `anim-*` groups for PPT step animations. **Presentation order differs from filenames** - follow the order below.

---

## Presentation Order

| # | Slide File | Title |
|---|------------|-------|
| 1 | [slide1_goal.svg](slide1_goal.svg) | Data Without Decisions |
| 2 | [slide6_fusion.svg](slide6_fusion.svg) | Prompt Beats Parsers |
| 3 | [slide2_frameworks.svg](slide2_frameworks.svg) | Agent Harness Shootout |
| 4 | [slide3_langchain_features.svg](slide3_langchain_features.svg) | Why LangChain Wins |
| 5 | [slide4_file_structure.svg](slide4_file_structure.svg) | Workspace Layout |
| 6 | [slide7_pydantic.svg](slide7_pydantic.svg) | Agent Pipeline Blocks |
| 7 | [slide5_adapter.svg](slide5_adapter.svg) | Model and Provider Choice |
| 8a | [slide8a_raw_scan.svg](slide8a_raw_scan.svg) | Before: Raw Scan Output |
| 8b | [slide8b_llm_report.svg](slide8b_llm_report.svg) | After: LLM Report + Tracking Hook |

---

## Slide 1: Data Without Decisions
* **Slide File:** [slide1_goal.svg](slide1_goal.svg)
* **Narration Script:**
  > "In Section 04, our scanner captured rich Kubernetes metadata — labels, CPU, memory, PVCs, orphan status. But the manual parser was brittle. Alias mismatches failed. There was no ticket draft. Just if-else rules that broke when policies changed.
  >
  > We have data — but no decisions. Time to upgrade the brain."

---

## Slide 2: Prompt Beats Parsers
* **Slide File:** [slide6_fusion.svg](slide6_fusion.svg)
* **Narration Script:**
  > "Instead of writing more parser code, we fuse three inputs into one LLM request: a system prompt defining the FinOps agent role, our tagging-rules.yaml policy, and live resource facts from the scanner.
  >
  > The PROMPT_TEMPLATE in analyzer.py blends them. If corporate policy changes tomorrow, you update the YAML — no Python changes required."
* **Live Demo Handoff:**
  > "Open `agent/analyzer.py` and locate `PROMPT_TEMPLATE`. Notice how `{tagging_rules}` and resource variables are injected."

---

## Slide 3: Agent Harness Shootout
* **Slide File:** [slide2_frameworks.svg](slide2_frameworks.svg)
* **Narration Script:**
  > "Before we build, let's compare harness options. AWS Bedrock, Azure OpenAI, and GCP Vertex AI are powerful but vendor-locked and harder to test locally.
  >
  > LangChain OSS gives us typed pipelines — prompt, llm, parser — with Pydantic outputs. That's exactly what FinOps automation needs. Not agent swarms — predictable structured decisions."

---

## Slide 4: Why LangChain Wins
* **Slide File:** [slide3_langchain_features.svg](slide3_langchain_features.svg)
* **Narration Script:**
  > "Four pillars: universal adapters via ChatOpenAI and base_url, prompt composition to inject K8s variables, Pydantic output parsing into ResourceDecision, and chain execution — one call per resource."

---

## Slide 5: Workspace Layout
* **Slide File:** [slide4_file_structure.svg](slide4_file_structure.svg)
* **Narration Script:**
  > "Here's our workspace. config/tagging-rules.yaml holds the policy. agent/analyzer.py has the LangChain logic. main.py orchestrates the scan-then-analyze loop. scanner.py collects K8s metadata. And .env holds our API credentials."
* **Live Demo Handoff:**
  > "Open the `05-llm-agent-langchain/` folder in your editor and walk through these files."

---

## Slide 6: Agent Pipeline Blocks
* **Slide File:** [slide7_pydantic.svg](slide7_pydantic.svg)
* **Narration Script:**
  > "The pipeline in main.py is straightforward: K8sScanner scans the cluster, PROMPT_TEMPLATE fuses policy with facts, ChatOpenAI runs inference, PydanticOutputParser molds the response into ResourceDecision, and generate_summary_report prints the final output.
  >
  > The chain is: prompt pipe llm pipe parser."

---

## Slide 7: Model and Provider Choice
* **Slide File:** [slide5_adapter.svg](slide5_adapter.svg)
* **Narration Script:**
  > "LangChain's ChatOpenAI is a universal adapter. Set OPENAI_BASE_URL, OPENAI_API_KEY, and OPENAI_MODEL_ID in .env. Same code works with KodeKloud, OpenAI, or a local LLM — just change the URL."
* **Live Demo Handoff:**
  > "Configure your `.env` with OPENAI_BASE_URL and OPENAI_API_KEY as shown in the guide."

---

## Slide 8a: Before — Raw Scan Output
* **Slide File:** [slide8a_raw_scan.svg](slide8a_raw_scan.svg)
* **Narration Script:**
  > "Remember Section 04's output? Dry violation lines — missing tag owner, missing cost-center. It told you what was wrong but not what to do about it."

---

## Slide 8b: After — LLM Report + Tracking Hook
* **Slide File:** [slide8b_llm_report.svg](slide8b_llm_report.svg)
* **Narration Script:**
  > "Now look at the LLM-enhanced report for the same payment-gateway-svc. Category unowned, priority high, a suggested fix, and a pre-drafted GitHub issue.
  >
  > The decisions are clear — but how do we track them? That's the handoff to Section 09."
* **Live Demo Handoff:**
  > "Run: `PYTHONPATH=sections/08-llm-agent-langchain python3 -m agent.main` and compare the output to Section 04."

---

## Animation Tips (PowerPoint)

- **slide6_fusion.svg**: Reveal `anim-input-system`, `anim-input-yaml`, `anim-input-facts` → arrows → `anim-reactor` → `anim-output`
- **slide2_frameworks.svg**: Cards L→R, LangChain card last with Winner badge
- **slide7_pydantic.svg**: Steps `anim-step-1` through `anim-step-5` sequentially
- **slide8a → slide8b**: Same resource name anchors the before/after transition
