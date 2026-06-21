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

## Slide 4A: Parser Logic Flow - CPU & Memory
*   **File**: [slide4a_parser_logic_flow.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide4a_parser_logic_flow.svg)
*   **Narrative Focus**:
    *   Walk through the **decision tree logic** inside `parse_cpu()` and `parse_memory()` functions
    *   Explain the **conditional branching**:
        *   CPU Parser: First checks if value is None (return 0), then checks if it ends with "m" (strip and return integer), else multiply by 1000
        *   Memory Parser: Checks suffix pattern (Gi/Mi/Ki/bytes) and applies correct conversion factor
    *   Emphasize this is **pattern matching logic** - the code inspects string format to determine which conversion formula to apply
    *   This prepares them to see the actual Python code in `collect.py` where these if-else chains live

---

## Slide 4B: Orphan Detection Logic Flow
*   **File**: [slide4b_orphan_detection_flow.svg](file:///Users/raghunandanask/Desktop/github-repo/k8-finops-agent/sections/04-local-python-agent/slides/slide4b_orphan_detection_flow.svg)
*   **Narrative Focus**:
    *   Explain the **3-step algorithm** using set operations:
        *   Step 1: Build a set of mounted PVCs by looping through all pods and extracting volume claims
        *   Step 2: Fetch all PVCs from Kubernetes API and parse their storage sizes
        *   Step 3: Use **set difference** logic - if PVC exists in all_pvcs but NOT in mounted_pvcs, flag as orphaned
    *   Show the **visual set comparison** (Venn diagram style) to illustrate the logic
    *   Highlight that this is a **membership test** (`if key NOT IN mounted_pvcs`) - simple but powerful
    *   This prepares them to see the actual `get_mounted_pvcs()` function and the orphan flagging loop in code

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
