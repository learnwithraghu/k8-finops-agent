"""Entry point for the agent-to-tracker integration.

Pipeline: scan Kubernetes metadata -> send each resource + the FinOps tagging
config to the LLM -> LLM creates tracker tickets directly via MCP tools.
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.analyzer import analyze_resource, generate_summary_report
from agent.scanner import K8sScanner
from agent.tracker import load_tracker_tools

TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"


def main():
    parser = argparse.ArgumentParser(
        description="K8s FinOps Agent - tracker integration"
    )
    parser.add_argument(
        "--mcp-url",
        default=None,
        help="Issue tracker MCP URL (default: http://localhost:8086/mcp)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    if Path(".env").exists():
        load_dotenv()

    model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1024"))
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

    if not api_key:
        logger.error("OPENAI_API_KEY not set in environment or .env file")
        sys.exit(1)

    mcp_url = args.mcp_url or os.getenv(
        "ISSUE_TRACKER_MCP_URL", "http://localhost:8086/mcp"
    )

    logger.info(f"Using OpenAI compatible model: {model_id}")
    logger.info(f"Using issue tracker MCP: {mcp_url}")

    # 0. Connect to tracker MCP and discover tools
    try:
        mcp_tools = asyncio.run(load_tracker_tools(mcp_url))
        logger.info(f"Connected to tracker MCP, tool: {list(mcp_tools.keys())}")
    except Exception as exc:
        logger.error(f"Failed to connect to issue tracker MCP: {exc}")
        logger.error("Start the Section 08 tracker first.")
        sys.exit(1)

    tagging_rules = yaml.safe_load(TAGGING_RULES_PATH.read_text()) or {}
    excluded_namespaces = tagging_rules.get("excluded_namespaces", []) or []

    # 1. Scan Kubernetes metadata
    scanner = K8sScanner(
        kubeconfig_path=os.getenv("KUBECONFIG_PATH"),
        excluded_namespaces=excluded_namespaces,
    )
    if not scanner.connect():
        logger.error("Failed to connect to Kubernetes")
        sys.exit(1)

    logger.info("Scanning resources in all namespaces")
    resources = scanner.scan_all()
    logger.info(f"Found {len(resources)} resources")

    # 2. Send each resource + tagging policy to the LLM.
    #    The LLM calls create_issue automatically for non-compliant resources.
    logger.info(f"Sending {len(resources)} resources to the LLM for decisions")
    results = []
    for resource in resources:
        try:
            decision = analyze_resource(
                resource,
                model_id,
                base_url,
                api_key,
                max_tokens,
                temperature,
                tagging_rules,
                mcp_tools=mcp_tools,
            )
            results.append((resource, decision))
        except Exception as e:
            logger.error(f"Failed to analyze {resource.namespace}/{resource.name}: {e}")

    # 3. Report
    report = generate_summary_report(results)
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80 + "\n")

    violation_count = sum(1 for _, d in results if not d.is_compliant)
    actionable = [(r, d) for r, d in results if d.should_create_issue]

    logger.info(f"Total resources analyzed: {len(results)}")
    logger.info(f"Violations: {violation_count}")
    logger.info(f"Actionable issues (filed by LLM): {len(actionable)}")

    logger.info("FinOps scan completed successfully")


if __name__ == "__main__":
    main()
