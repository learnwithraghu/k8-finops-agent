# Slide Presentation Guide: Section 04 Local Python Agent

This guide accompanies the generated SVG slide assets to help you narrate this section before jumping into the live demo.

---

## Slide 1: Section Goal & Overview
*   **File**: [slide1_overview.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide1_overview.svg)
*   **Narrative Focus**:
    *   Explain the problem: Live cluster state is dynamic and complex. To perform FinOps cost optimization and audit tag compliance, we first need to capture raw facts.
    *   Introduce the solution: A simple Python agent (`collect.py`) that acts as a dumb pipe, querying the Kubernetes cluster and outputting a standardized, clean `k8s_metadata.json` dataset.
    *   Highlight: We intentionally separate collection from decisions. The agent makes no assumptions about compliance.

---

## Slide 2: Architecture Overview
*   **File**: [slide2_architecture.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide2_architecture.svg)
*   **Narrative Focus**:
    *   How the data flows: Explain the inputs (`tagging-rules.yaml` defining excluded namespaces and the active `kubeconfig` establishing context).
    *   Inside the engine: The agent processes namespaces dynamically, filters out the clutter, standardizes heterogeneous cluster units (such as CPU cores and memory sizes), and outputs a clean JSON file.

---

## Slide 3: Code Blocks & Workspace Layout
*   **File**: [slide3_file_structure.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide3_file_structure.svg)
*   **Narrative Focus**:
    *   Explain the layout of the code in Section 04:
        *   `config/tagging-rules.yaml`: Defines target labels and system namespace exclusions.
        *   `agent/collect.py`: Holds the extraction and normalization logic.
        *   `requirements.txt`: Manages clean external dependencies (`kubernetes`, `pyyaml`, `python-dotenv`).

---

## Slide 4: Parser Methods Needed
*   **File**: [slide4_parser_methods.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide4_parser_methods.svg)
*   **Narrative Focus**:
    *   Explain why we need custom parser methods in the agent:
        *   Kubernetes returns values in varying units (e.g., CPU request of `"1.5"` vs `"500m"`, and Memory of `"256Mi"` vs `"1Gi"`). We normalize these to integers (`millicores` and `MiB`) so they are standard.
        *   We detect **orphaned PVCs** by scanning all Pod volume mounts and comparing them with the total PVC list. Any PVC not mounted is flagged as an orphan.

---

## Slide 5: Analyzing the Output JSON
*   **File**: [slide5_json_analysis.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide5_json_analysis.svg)
*   **Narrative Focus**:
    *   Walk the audience through the structure of the JSON payload.
    *   Point out what is present: flat metadata blocks, structured resources, normalized metrics.
    *   Crucially point out **what is missing**: There is no compliance checking, cost calculations, or remediation alerts here. It's just a raw dump.

---

## Slide 6: The Handoff Dilemma (Open Questions)
*   **File**: [slide6_the_dilemma.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide6_the_dilemma.svg)
*   **Narrative Focus**:
    *   Raise the core architectural question: *"We now have the raw facts in JSON and the policy rules in YAML. How do we map them to find compliance issues?"*
    *   **Option A (Brute Force)**: Write thousands of lines of nested `if-else` loops. Explain why this is brittle: tag aliases change, exceptions occur, and maintaining it becomes a codebase nightmare.
    *   **Option B (LLM Agent)**: Introduce the next section. Instead of hardcoding rules, we feed the JSON state + YAML policy to an LLM Reasoning Engine (LangChain/Bedrock) that can dynamically analyze compliance and draft fixes for us.
