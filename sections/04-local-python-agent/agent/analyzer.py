"""AWS Bedrock AI analyzer for FinOps agent."""

import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

import boto3
from botocore.exceptions import ClientError

from agent.scanner import K8sResource
from agent.untracked_money import UntrackedMoney

logger = logging.getLogger(__name__)


@dataclass
class AIRecommendation:
    """AI-generated recommendation for a resource."""
    suggested_cost_center: str
    suggested_owner: str
    suggested_tags: Dict[str, str]
    priority: str  # critical, high, medium, low
    reasoning: str
    estimated_savings: float


@dataclass
class IssueDraft:
    """Bedrock-generated GitHub issue payload."""
    title: str
    body: str
    labels: List[str]
    priority: str
    should_create_issue: bool
    reasoning: str
    suggested_cost_center: str
    suggested_owner: str
    suggested_tags: Dict[str, str]
    estimated_savings: float


class BedrockAnalyzer:
    """Generates issue drafts using AWS Bedrock."""

    def __init__(
        self,
        model_id: Optional[str] = None,
        region: Optional[str] = None,
        role_arn: Optional[str] = None,
        session_token: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.3,
        tagging_rules: Optional[Dict[str, Any]] = None,
    ):
        self.model_id = model_id or "anthropic.claude-3-5-haiku-20241022-v1:0"
        self.region = region or "us-east-1"
        self.role_arn = role_arn
        self.session_token = session_token
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tagging_rules = tagging_rules or {}
        self.bedrock_runtime = None
        self._connected = False

    def connect(self) -> bool:
        """Connect to AWS Bedrock (optionally by assuming a role)."""
        try:
            session_kwargs = {"region_name": self.region}
            if self.session_token:
                session_kwargs["aws_session_token"] = self.session_token

            session = boto3.Session(**session_kwargs)

            if self.role_arn:
                sts = session.client("sts")
                assumed = sts.assume_role(
                    RoleArn=self.role_arn,
                    RoleSessionName="k8-finops-agent"
                )["Credentials"]
                session = boto3.Session(
                    aws_access_key_id=assumed["AccessKeyId"],
                    aws_secret_access_key=assumed["SecretAccessKey"],
                    aws_session_token=assumed["SessionToken"],
                    region_name=self.region,
                )
                logger.info(f"Assumed role for Bedrock access: {self.role_arn}")

            self.bedrock_runtime = session.client("bedrock-runtime", region_name=self.region)
            self._connected = True
            logger.info(f"Connected to AWS Bedrock using inference profile ARN: {self.model_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Bedrock: {e}")
            return False

    def _build_prompt(self, resource: K8sResource, untracked: UntrackedMoney) -> str:
        """Build prompt for AI issue drafting."""
        logger.info(
            f"Sending resource to Bedrock: {resource.namespace}/{resource.name} ({resource.kind})"
        )
        return f"""You are a FinOps agent for a Kubernetes-based airline platform.

Review the following resource and produce a GitHub issue draft.
Return ONLY valid JSON.

Resource Facts:
- Name: {resource.name}
- Namespace: {resource.namespace}
- Kind: {resource.kind}
- Labels: {json.dumps(resource.labels, indent=2)}
- Annotations: {json.dumps(resource.annotations, indent=2)}
- CPU Request: {resource.cpu_request}m
- Memory Request: {resource.memory_request}Mi
- Replicas: {resource.replicas}
- PVCs: {resource.pvc_names}
- PVC Size (GB): {resource.pvc_size_gb}
- Orphaned PVC: {resource.is_orphaned}
- Monthly Cost: ${untracked.monthly_cost:.2f}
- Untracked Amount: ${untracked.untracked_amount:.2f}
- Category: {untracked.category.value}
- Missing Tags: {', '.join(str(t) for t in untracked.missing_tags if t) if untracked.missing_tags else 'None'}
- Reason: {untracked.reason}

Tagging Policy:
{json.dumps(self.tagging_rules, indent=2)}

JSON schema:
{{
  "should_create_issue": true,
  "issue_title": "[FinOps] namespace/name - CATEGORY ($X.XX/month)",
  "issue_body": "markdown body",
  "issue_labels": ["finops", "category:...", "kind:..."],
  "priority": "critical|high|medium|low",
  "reasoning": "short explanation",
  "suggested_cost_center": "...",
  "suggested_owner": "...",
  "suggested_tags": {{"cost-center": "...", "owner": "..."}},
  "estimated_monthly_savings": 0.0
}}

Rules:
- Use the tagging policy and airline context.
- Prefer concrete team names.
- Set should_create_issue=false only if this is clearly not actionable.
- Keep titles concise.
- Body should include: summary, cost impact, missing tags, and remediation steps.
"""

    def _invoke_model(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Invoke Bedrock model with prompt."""
        if not self._connected:
            logger.error("Bedrock not connected")
            return None

        try:
            messages = [
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ]

            if hasattr(self.bedrock_runtime, "converse"):
                response = self.bedrock_runtime.converse(
                    modelId=self.model_id,
                    messages=messages,
                    inferenceConfig={
                        "maxTokens": self.max_tokens,
                        "temperature": self.temperature,
                        "topP": 0.9,
                    },
                )
                text = response["output"]["message"]["content"][0]["text"]
            else:
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "messages": [{"role": "user", "content": prompt}],
                })
                response = self.bedrock_runtime.invoke_model(
                    body=body,
                    modelId=self.model_id,
                    accept="application/json",
                    contentType="application/json",
                )
                response_body = json.loads(response.get("body").read())
                content = response_body.get("content", [])
                if not content:
                    return None
                text = content[0].get("text", "")

            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])

            logger.warning(f"Bedrock response did not contain JSON: {text}")
            return None
        except ClientError as e:
            logger.error(f"Bedrock API error: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error invoking Bedrock: {e}")
            return None

    def _fallback_issue_draft(self, resource: K8sResource, untracked: UntrackedMoney) -> IssueDraft:
        """Deterministic fallback if Bedrock output is unavailable."""
        labels = [
            "finops",
            f"category:{untracked.category.value}",
            f"kind:{resource.kind.lower()}",
        ]
        priority = "critical" if untracked.untracked_amount >= 50 else ("high" if untracked.untracked_amount >= 20 else "medium")
        body = f"""## Summary

{untracked.reason}

## Resource Details
- **Name**: {resource.name}
- **Namespace**: {resource.namespace}
- **Kind**: {resource.kind}
- **Monthly Cost**: ${untracked.monthly_cost:.2f}
- **Untracked Amount**: ${untracked.untracked_amount:.2f}
- **Missing Tags**: {', '.join(str(t) for t in untracked.missing_tags if t) if untracked.missing_tags else 'None'}

## Remediation
1. Add the missing labels/tags.
2. Update the manifest so the fix persists.
3. Re-run the FinOps scan.
"""
        return IssueDraft(
            title=f"[FinOps] {resource.namespace}/{resource.name} - {untracked.category.value.upper()} (${untracked.untracked_amount:.2f}/month)",
            body=body,
            labels=labels,
            priority=priority,
            should_create_issue=True,
            reasoning=untracked.reason,
            suggested_cost_center="unknown",
            suggested_owner="unknown",
            suggested_tags={},
            estimated_savings=untracked.untracked_amount,
        )

    def analyze_resource(self, resource: K8sResource, untracked: UntrackedMoney) -> Optional[IssueDraft]:
        """Analyze a resource and return a GitHub issue draft."""
        prompt = self._build_prompt(resource, untracked)
        result = self._invoke_model(prompt)

        if not result:
            return self._fallback_issue_draft(resource, untracked)

        should_create = bool(result.get("should_create_issue", True))
        title = result.get("issue_title") or f"[FinOps] {resource.namespace}/{resource.name} - {untracked.category.value.upper()} (${untracked.untracked_amount:.2f}/month)"
        body = result.get("issue_body") or self._fallback_issue_draft(resource, untracked).body
        labels = result.get("issue_labels") or ["finops", f"category:{untracked.category.value}", f"kind:{resource.kind.lower()}"]

        return IssueDraft(
            title=title,
            body=body,
            labels=list(dict.fromkeys(labels)),
            priority=result.get("priority", "medium"),
            should_create_issue=should_create,
            reasoning=result.get("reasoning", untracked.reason),
            suggested_cost_center=result.get("suggested_cost_center", "unknown"),
            suggested_owner=result.get("suggested_owner", "unknown"),
            suggested_tags=result.get("suggested_tags", {}),
            estimated_savings=float(result.get("estimated_monthly_savings", untracked.untracked_amount)),
        )

    def analyze_batch(self, violations: List[tuple]) -> Dict[str, Any]:
        """Analyze multiple violations and return summary."""
        results = []
        total_savings = 0.0

        for resource, untracked in violations:
            draft = self.analyze_resource(resource, untracked)
            if draft:
                results.append({
                    'resource': f"{resource.namespace}/{resource.name}",
                    'kind': resource.kind,
                    'current_cost': untracked.monthly_cost,
                    'untracked_amount': untracked.untracked_amount,
                    'issue': {
                        'title': draft.title,
                        'priority': draft.priority,
                        'should_create_issue': draft.should_create_issue,
                        'reasoning': draft.reasoning,
                        'labels': draft.labels,
                    }
                })
                total_savings += draft.estimated_savings

        return {
            'analyzed_count': len(violations),
            'recommendations': results,
            'total_estimated_savings': round(total_savings, 2)
        }

    def generate_summary_report(self, untracked_analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary report."""
        report = f"""# FinOps Analysis Report (LLM Powered - Mock)

## Cost Summary
- **Total Monthly Cost**: ${untracked_analysis['total_monthly_cost']}
- **Tracked**: ${untracked_analysis['total_tracked']} ({untracked_analysis['tracked_percentage']}%)
- **Untracked**: ${untracked_analysis['total_untracked']} ({untracked_analysis['untracked_percentage']}%)

## Breakdown by Category
"""

        for category, amount in untracked_analysis.get('breakdown_by_category', {}).items():
            report += f"- **{category.capitalize()}**: ${amount}/month\n"

        report += f"\n## Violations Found: {len(untracked_analysis.get('violations', []))}\n\n"

        for i, v in enumerate(untracked_analysis.get('violations', []), 1):
            report += f"""### {i}. {v['resource']} ({v['kind']})
- **Category**: {v['category']}
- **Monthly Cost**: ${v['monthly_cost']}
- **Untracked Amount**: ${v['untracked_amount']}
- **Missing Tags**: {', '.join(str(t) for t in v['missing_tags'] if t) if v['missing_tags'] else 'None'}
- **Reason**: {v['reason']}

"""

        return report


class MockAnalyzer:
    """Mock analyzer for testing without Bedrock."""

    def __init__(self):
        self._connected = True

    def connect(self) -> bool:
        logger.info("Using mock analyzer (no Bedrock connection)")
        return True

    def analyze_resource(self, resource: K8sResource, untracked: UntrackedMoney) -> Optional[IssueDraft]:
        name_lower = resource.name.lower()

        if 'flight' in name_lower or 'search' in name_lower:
            cost_center = "booking-engine"
            owner = "booking-team"
        elif 'booking' in name_lower:
            cost_center = "booking-engine"
            owner = "booking-team"
        elif 'payment' in name_lower:
            cost_center = "payment"
            owner = "payment-team"
        elif 'inventory' in name_lower:
            cost_center = "inventory"
            owner = "inventory-team"
        else:
            cost_center = "platform"
            owner = "platform-team"

        priority = "high" if untracked.untracked_amount > 20 else "medium"
        labels = ["finops", f"category:{untracked.category.value}", f"kind:{resource.kind.lower()}"]
        body = f"""## Summary

{untracked.reason}

## Suggested Tags
- **cost-center**: {cost_center}
- **owner**: {owner}

## Resource Details
- **Name**: {resource.name}
- **Namespace**: {resource.namespace}
- **Kind**: {resource.kind}
- **Monthly Cost**: ${untracked.monthly_cost:.2f}
- **Untracked Amount**: ${untracked.untracked_amount:.2f}
"""

        return IssueDraft(
            title=f"[FinOps] {resource.namespace}/{resource.name} - {untracked.category.value.upper()} (${untracked.untracked_amount:.2f}/month)",
            body=body,
            labels=labels,
            priority=priority,
            should_create_issue=True,
            reasoning=f"Based on resource name '{resource.name}', this appears to be part of the {cost_center} system.",
            suggested_cost_center=cost_center,
            suggested_owner=owner,
            suggested_tags={
                'cost-center': cost_center,
                'owner': owner,
                'environment': 'prod',
                'application': resource.name,
                'tier': 'backend'
            },
            estimated_savings=untracked.untracked_amount,
        )

    def analyze_batch(self, violations: List[tuple]) -> Dict[str, Any]:
        results = []
        total_savings = 0.0

        for resource, untracked in violations:
            draft = self.analyze_resource(resource, untracked)
            if draft:
                results.append({
                    'resource': f"{resource.namespace}/{resource.name}",
                    'kind': resource.kind,
                    'current_cost': untracked.monthly_cost,
                    'untracked_amount': untracked.untracked_amount,
                    'issue': {
                        'title': draft.title,
                        'priority': draft.priority,
                        'should_create_issue': draft.should_create_issue,
                        'reasoning': draft.reasoning,
                        'labels': draft.labels,
                    }
                })
                total_savings += draft.estimated_savings

        return {
            'analyzed_count': len(violations),
            'recommendations': results,
            'total_estimated_savings': round(total_savings, 2)
        }

    def generate_summary_report(self, untracked_analysis: Dict[str, Any]) -> str:
        report = f"""# FinOps Analysis Report (LLM Powered - Bedrock)

## Cost Summary
- **Total Monthly Cost**: ${untracked_analysis['total_monthly_cost']}
- **Tracked**: ${untracked_analysis['total_tracked']} ({untracked_analysis['tracked_percentage']}%)
- **Untracked**: ${untracked_analysis['total_untracked']} ({untracked_analysis['untracked_percentage']}%)

## Breakdown by Category
"""

        for category, amount in untracked_analysis.get('breakdown_by_category', {}).items():
            report += f"- **{category.capitalize()}**: ${amount}/month\n"

        report += f"\n## Violations Found: {len(untracked_analysis.get('violations', []))}\n\n"

        for i, v in enumerate(untracked_analysis.get('violations', []), 1):
            report += f"""### {i}. {v['resource']} ({v['kind']})
- **Category**: {v['category']}
- **Monthly Cost**: ${v['monthly_cost']}
- **Untracked Amount**: ${v['untracked_amount']}
- **Missing Tags**: {', '.join(str(t) for t in v['missing_tags'] if t) if v['missing_tags'] else 'None'}
- **Reason**: {v['reason']}

"""

        return report
