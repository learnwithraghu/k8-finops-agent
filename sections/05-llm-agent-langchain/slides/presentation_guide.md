# Section 05: LLM Decision Flow — Slide Guide & Narrative

This guide provides the slide-by-slide narration scripts, visual metaphor explanations, and live demo handoff instructions for presenting **Section 05: LLM Decision Flow**.

> **Design System**: All slides use the `create-presentation-svgs` skill with `infographic-metaphor` integration. White backgrounds, reusable `<defs>` icons (pod, warning, brain, check, cross, configmap), AWS/GCP color palette, IDE-styled code blocks (dark), and clean connections. Canvas: `viewBox="0 0 1280 720"` (16:9).

---

## Slide 1: Section Goal & Overview
* **Slide File:** [slide1_goal.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide1_goal.svg)
* **Visual Metaphor:** Upgrading the Brain. A mechanical circuit switch (static rules) transforms into a glowing neural core (LLM agent). Cross icons mark limitations; check icons mark capabilities.
* **Narration Script:**
  > "Welcome to Section 5. In the previous section, we built a standard Python script that checked tags. It was fast, but it had a massive limitation: it was brittle and couldn't think. If a tag was named 'owner-team' instead of 'owner', it failed. If a resource was orphaned, it couldn't tell you who to contact or write a ticket.
  >
  > Today, we are upgrading the brain of our collector. We are moving from hardcoded static loops to an LLM-powered decision engine using LangChain. We'll feed raw metadata and policies directly into the LLM so it can handle context matching, categorizations, and ticket planning automatically."
* **Live Demo Handoff:**
  > "Let's first take a look at the files in this section. Open up your code editor and look inside the `sections/05-llm-agent-langchain/` directory to see the setup."

---

## Slide 2: The Universal LLM Adapter
* **Slide File:** [slide2_adapter.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide2_adapter.svg)
* **Visual Metaphor:** A universal travel adapter plug. An IDE-styled `.env` window on the left shows syntax-highlighted config. The central adapter hub branches to three provider endpoints (OpenAI, KodeKloud, Local), with the active one highlighted.
* **Narration Script:**
  > "One of the major strengths of using LangChain's `ChatOpenAI` client is that it is provider-agnostic. Think of it like a universal travel adapter. You write the code once, and by simply modifying your `.env` configuration file, you can plug it into OpenAI, an open-source model running on your local machine, or a managed gateway like the KodeKloud AI Gateway.
  >
  > In this section, we config our `.env` parameters: `OPENAI_BASE_URL` points to the KodeKloud gateway, and `OPENAI_API_KEY` is loaded securely without hardcoding secrets in python scripts."
* **Live Demo Handoff:**
  > "Let's configure our environment. Open the `.env` file and set up the `OPENAI_BASE_URL` and `OPENAI_API_KEY` credentials as shown in Step 3 & 4 of the guide."

---

## Slide 3: Prompt Template & Policy Fusion
* **Slide File:** [slide3_fusion.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide3_fusion.svg)
* **Visual Metaphor:** A fusion reactor. Two distinct data feeds (blue K8s metadata + orange FinOps policy) converge into a purple-gradient prompt template reactor, which outputs to a green LLM inference node. Dashed connection lines with arrowheads show data flow.
* **Narration Script:**
  > "So, how does the LLM actually know our policies? Instead of writing complex parser rules in Python, we use Prompt Engineering to fuse two separate sources of data.
  >
  > First, we feed the raw live Kubernetes resource metadata (JSON). Second, we feed the corporate FinOps YAML policy block. We blend them into a single Prompt Template. The LLM receives both as context and applies the policies itself. This means if your corporate policies change tomorrow, you only update the YAML file—no code changes are required."
* **Live Demo Handoff:**
  > "Let's inspect the prompt layout. Open `sections/05-llm-agent-langchain/agent/analyzer.py` and inspect the `PROMPT_TEMPLATE` and how it references `{resource_name}` and `{tagging_rules}` variables."

---

## Slide 4: Structured Outputs with Pydantic
* **Slide File:** [slide4_pydantic.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide4_pydantic.svg)
* **Visual Metaphor:** A metal stencil/mold. Amorphous unstructured text (cloud shape) enters the Pydantic schema mold (typed field slots with color-coded type indicators), and emerges as a rigid, structured `ResourceDecision` instance ready for API consumption.
* **Narration Script:**
  > "LLMs naturally communicate in paragraphs of text. But our automation pipelines need structured data—integers, boolean values, and specific keys.
  >
  > To solve this, we use LangChain's `PydanticOutputParser`. We define a rigid Python class called `ResourceDecision` with typed fields. The parser inserts instructions into the LLM prompt telling it how to structure the JSON output. When the LLM answers, the parser molds that raw string response directly into our typed Python object, ready to be passed downstream to APIs."
* **Live Demo Handoff:**
  > "Let's view the schema definition. Open `sections/05-llm-agent-langchain/agent/analyzer.py` and locate the `ResourceDecision` Pydantic class to see the structured fields."

---

## Slide 5: Raw Scan vs. LLM-Enhanced Report
* **Slide File:** [slide5_comparison.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide5_comparison.svg)
* **Visual Metaphor:** X-Ray vs. Prescription. A terminal-styled raw CLI output (left) shows bare violations. A rich decision report (right) displays categorized resource cards with priority badges, suggested fixes, owner routing, and auto-drafted ticket content. A central "VS" badge anchors the comparison.
* **Narration Script:**
  > "Finally, let's look at the result. In Section 4, our CLI printed raw fact violations. It just said 'Missing Tag Owner'. It was dry, non-contextual, and required manual interpretation.
  >
  > With our LLM upgrade in Section 5, we get a rich, decision-oriented report. It lists compliance categories, reasoning, and suggested fixes, and even pre-drafts the exact title and body for a GitHub ticket. It turns raw information into a clear prescription for remediation."
* **Live Demo Handoff:**
  > "Let's run the completed code! Execute the agent in your terminal: `PYTHONPATH=sections/05-llm-agent-langchain python3 -m agent.main` and look at the new LLM-powered console output report!"

---

## Slide 6: The Bridge Metaphor *(Infographic-Metaphor Skill)*
* **Slide File:** [slide6_bridge_metaphor.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide6_bridge_metaphor.svg)
* **Skill Invocation:** `infographic-metaphor` with `title="Bridging K8s Data to FinOps Decisions"`, `metaphor="bridge"`, `components=["cluster","json","python-agent","brain"]`, `palette="aws"`
* **Visual Metaphor:** Two cliff islands separated by a water chasm (complexity gap). The left island holds raw K8s metadata (pod icons, JSON cards). The right island holds structured FinOps decisions (compliance reports, auto-drafted tickets). A bridge structure spans the gap with the LLM brain icon at its center. Data flows across the bridge from raw JSON/YAML inputs to structured `ResourceDecision` outputs.
* **Narration Script:**
  > "Let me give you a mental model for what we're building. Think of raw Kubernetes cluster data — pods, services, PVCs — sitting on one island. On the other island, you have the FinOps decisions your organization needs: compliance reports, ownership assignments, and remediation tickets.
  >
  > Between them? A chasm of complexity — manual triage, context loss, and interpretation overhead. The LLM agent we built with LangChain is the bridge. It takes raw metadata and policy rules in, and outputs structured, actionable decisions. Without the bridge, your data stays stranded."
* **When to Use:**
  > Use this slide as a summary/recap after walking through all the technical details, or as a visual anchor when introducing the section to non-technical stakeholders.
