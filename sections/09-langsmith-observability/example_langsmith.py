"""Minimal LangSmith trace example.

Loads LLM and LangSmith settings from the repo-root `.env`.
With LANGSMITH_TRACING=true, nested @traceable spans and the LLM call
show up in LANGSMITH_PROJECT (see `.env.example`).
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langsmith import traceable

load_dotenv(Path(__file__).parents[2] / ".env")

PROMPT = (
    "In one sentence, explain why an observability trace helps debug "
    "a Kubernetes FinOps policy auditor."
)


def build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL_ID"],
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "512")),
    )


@traceable(name="fetch_mock_cluster_context")
def fetch_mock_cluster_context() -> str:
    """Child span: stand-in for MCP kubectl_get data."""
    return (
        "namespaces: booking, payment; 12 total; "
        "3 deployments missing cost-center label"
    )


@traceable(name="finops_trace_demo")
def run_trace_demo() -> str:
    """Parent span: gather mock cluster context, then ask the LLM."""
    context = fetch_mock_cluster_context()
    llm = build_llm()
    response = llm.invoke(
        [
            HumanMessage(
                content=f"Cluster context:\n{context}\n\n{PROMPT}",
            )
        ]
    )
    return response.content


def main() -> None:
    if os.getenv("LANGSMITH_TRACING", "").lower() not in ("true", "1", "yes"):
        print("Warning: LANGSMITH_TRACING is not enabled — set it in .env to send traces.")

    answer = run_trace_demo()
    print(answer)

    project = os.getenv("LANGSMITH_PROJECT", "default")
    print(f"\nTrace sent to LangSmith project: {project}")
    print("Open https://smith.langchain.com to inspect parent and child spans.")


if __name__ == "__main__":
    main()
