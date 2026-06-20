# Section 05: LLM Decision Flow — Slide Guide & Narrative

This guide provides the slide-by-slide narration scripts, visual metaphor explanations, and live demo handoff instructions for presenting **Section 05: LLM Decision Flow**.

---

## Slide 1: Section Goal & Overview
* **Slide File:** [slide1_goal.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide1_goal.svg)
* **Visual Metaphor:** Upgrading the Brain. Transitioning from a basic mechanical switch to an intelligent neural core.
* **Narration Script:**
  > "Welcome to Section 5. In the previous section, we built a standard Python script that checked tags. It was fast, but it had a massive limitation: it was brittle and couldn't think. If a tag was named 'owner-team' instead of 'owner', it failed. If a resource was orphaned, it couldn't tell you who to contact or write a ticket.
  >
  > Today, we are upgrading the brain of our collector. We are moving from hardcoded static loops to an LLM-powered decision engine using LangChain. We'll feed raw metadata and policies directly into the LLM so it can handle context matching, categorizations, and ticket planning automatically."
* **Live Demo Handoff:**
  > "Let's first take a look at the files in this section. Open up your code editor and look inside the `sections/05-llm-agent-langchain/` directory to see the setup."

---

## Slide 2: The Universal LLM Adapter
* **Slide File:** [slide2_adapter.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide2_adapter.svg)
* **Visual Metaphor:** A multi-nation power adapter plug. One unified interface matching various backend sockets.
* **Narration Script:**
  > "One of the major strengths of using LangChain's `ChatOpenAI` client is that it is provider-agnostic. Think of it like a universal travel adapter. You write the code once, and by simply modifying your `.env` configuration file, you can plug it into OpenAI, an open-source model running on your local machine, or a managed gateway like the KodeKloud AI Gateway.
  >
  > In this section, we config our `.env` parameters: `OPENAI_BASE_URL` points to the KodeKloud gateway, and `OPENAI_API_KEY` is loaded securely without hardcoding secrets in python scripts."
* **Live Demo Handoff:**
  > "Let's configure our environment. Open the `.env` file and set up the `OPENAI_BASE_URL` and `OPENAI_API_KEY` credentials as shown in Step 3 & 4 of the guide."

---

## Slide 3: Prompt Template & Policy Fusion
* **Slide File:** [slide3_fusion.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide3_fusion.svg)
* **Visual Metaphor:** A chemical fusion reactor or blender mixing two distinct feed inputs to generate a unified chemical output.
* **Narration Script:**
  > "So, how does the LLM actually know our policies? Instead of writing complex parser rules in Python, we use Prompt Engineering to fuse two separate sources of data.
  >
  > First, we feed the raw live Kubernetes resource metadata (JSON). Second, we feed the corporate FinOps YAML policy block. We blend them into a single Prompt Template. The LLM receives both as context and applies the policies itself. This means if your corporate policies change tomorrow, you only update the YAML file—no code changes are required."
* **Live Demo Handoff:**
  > "Let's inspect the prompt layout. Open `sections/05-llm-agent-langchain/agent/analyzer.py` and inspect the `PROMPT_TEMPLATE` and how it references `{resource_name}` and `{tagging_rules}` variables."

---

## Slide 4: Structured Outputs with Pydantic
* **Slide File:** [slide4_pydantic.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide4_pydantic.svg)
* **Visual Metaphor:** A metal stencil/mold. Liquid text goes in; rigid, standardized key-value blocks come out.
* **Narration Script:**
  > "LLMs naturally communicate in paragraphs of text. But our automation pipelines need structured data—integers, boolean values, and specific keys.
  >
  > To solve this, we use LangChain's `PydanticOutputParser`. We define a rigid Python class called `ResourceDecision` with typed fields. The parser inserts instructions into the LLM prompt telling it how to structure the JSON output. When the LLM answers, the parser molds that raw string response directly into our typed Python object, ready to be passed downstream to APIs."
* **Live Demo Handoff:**
  > "Let's view the schema definition. Open `sections/05-llm-agent-langchain/agent/analyzer.py` and locate the `ResourceDecision` Pydantic class to see the structured fields."

---

## Slide 5: Raw Scan vs. LLM-Enhanced Report
* **Slide File:** [slide5_comparison.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/05-llm-agent-langchain/slides/slide5_comparison.svg)
* **Visual Metaphor:** Black-and-white diagnostic X-Ray vs. a comprehensive medical prescription/remediation plan.
* **Narration Script:**
  > "Finally, let's look at the result. In Section 4, our CLI printed raw fact violations. It just said 'Missing Tag Owner'. It was dry, non-contextual, and required manual interpretation.
  >
  > With our LLM upgrade in Section 5, we get a rich, decision-oriented report. It lists compliance categories, reasoning, and suggested fixes, and even pre-drafts the exact title and body for a GitHub ticket. It turns raw information into a clear prescription for remediation."
* **Live Demo Handoff:**
  > "Let's run the completed code! Execute the agent in your terminal: `PYTHONPATH=sections/05-llm-agent-langchain python3 -m agent.main` and look at the new LLM-powered console output report!"
