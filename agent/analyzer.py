"""AWS Bedrock AI analyzer for FinOps agent."""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

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


class BedrockAnalyzer:
    """Analyzes resources using AWS Bedrock Haiku model."""

    def __init__(self, model_id: Optional[str] = None, region: Optional[str] = None):
        """Initialize Bedrock client."""
        self.model_id = model_id or "anthropic.claude-3-haiku-20240307-v1:0"
        self.region = region or "us-east-1"
        self.bedrock_runtime = None
        self._connected = False

    def connect(self) -> bool:
        """Connect to AWS Bedrock."""
        try:
            self.bedrock_runtime = boto3.client(
                service_name="bedrock-runtime",
                region_name=self.region
            )
            self._connected = True
            logger.info(f"Connected to AWS Bedrock ({self.model_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Bedrock: {e}")
            return False

    def _build_prompt(self, resource: K8sResource, untracked: UntrackedMoney) -> str:
        """Build prompt for AI analysis."""
        prompt = f"""You are a FinOps expert analyzing Kubernetes resources for an airline booking system.

Resource Details:
- Name: {resource.name}
- Namespace: {resource.namespace}
- Kind: {resource.kind}
- Current Labels: {json.dumps(resource.labels, indent=2)}
- CPU Request: {resource.cpu_request}m
- Memory Request: {resource.memory_request}Mi
- Replicas: {resource.replicas}
- Monthly Cost: ${untracked.monthly_cost:.2f}
- Untracked Amount: ${untracked.untracked_amount:.2f}
- Missing Tags: {', '.join(untracked.missing_tags)}
- Issue: {untracked.reason}

Context: This is an airline booking system with these cost centers:
- booking-engine (core booking logic)
- payment (payment processing)
- inventory (flight/hotel inventory)
- customer-service (support tools)
- analytics (data/analytics)
- platform (shared infrastructure)

Based on the resource name "{resource.name}", suggest the appropriate:
1. cost-center (choose from the list above)
2. owner (team name like "booking-team", "payment-team", "platform-team")
3. Any other missing tags

Respond in JSON format:
{{
    "suggested_cost_center": "...",
    "suggested_owner": "...",
    "suggested_tags": {{
        "cost-center": "...",
        "owner": "...",
        "environment": "...",
        "application": "...",
        "tier": "..."
    }},
    "priority": "critical|high|medium|low",
    "reasoning": "...",
    "estimated_monthly_savings": 0.0
}}"""
        return prompt

    def _invoke_model(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Invoke Bedrock model with prompt."""
        if not self._connected:
            logger.error("Bedrock not connected")
            return None

        try:
            # Anthropic Claude message format
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": 0.3,
                "messages": messages
            })

            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )

            response_body = json.loads(response.get('body').read())
            content = response_body.get('content', [])

            if content and len(content) > 0:
                text = content[0].get('text', '')
                # Try to parse JSON from response
                try:
                    # Find JSON in the response
                    start = text.find('{')
                    end = text.rfind('}') + 1
                    if start >= 0 and end > start:
                        json_str = text[start:end]
                        return json.loads(json_str)
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse JSON from response: {text}")
                    return None

            return None

        except ClientError as e:
            logger.error(f"Bedrock API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error invoking Bedrock: {e}")
            return None

    def analyze_resource(self, resource: K8sResource, untracked: UntrackedMoney) -> Optional[AIRecommendation]:
        """Analyze a resource and get AI recommendations."""
        prompt = self._build_prompt(resource, untracked)
        result = self._invoke_model(prompt)

        if result:
            return AIRecommendation(
                suggested_cost_center=result.get('suggested_cost_center', 'unknown'),
                suggested_owner=result.get('suggested_owner', 'unknown'),
                suggested_tags=result.get('suggested_tags', {}),
                priority=result.get('priority', 'medium'),
                reasoning=result.get('reasoning', ''),
                estimated_savings=result.get('estimated_monthly_savings', 0.0)
            )
        return None

    def analyze_batch(self, violations: List[tuple]) -> Dict[str, Any]:
        """Analyze multiple violations and return summary."""
        results = []
        total_savings = 0.0

        for resource, untracked in violations:
            recommendation = self.analyze_resource(resource, untracked)
            if recommendation:
                results.append({
                    'resource': f"{resource.namespace}/{resource.name}",
                    'kind': resource.kind,
                    'current_cost': untracked.monthly_cost,
                    'untracked_amount': untracked.untracked_amount,
                    'suggestion': {
                        'cost_center': recommendation.suggested_cost_center,
                        'owner': recommendation.suggested_owner,
                        'tags': recommendation.suggested_tags,
                        'priority': recommendation.priority,
                        'reasoning': recommendation.reasoning,
                        'estimated_savings': recommendation.estimated_savings
                    }
                })
                total_savings += recommendation.estimated_savings

        return {
            'analyzed_count': len(violations),
            'recommendations': results,
            'total_estimated_savings': round(total_savings, 2)
        }

    def generate_summary_report(self, untracked_analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary report."""
        report = f"""# FinOps Analysis Report

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
- **Missing Tags**: {', '.join(v['missing_tags']) if v['missing_tags'] else 'None'}
- **Reason**: {v['reason']}

"""

        return report


class MockAnalyzer:
    """Mock analyzer for testing without Bedrock."""

    def __init__(self):
        """Initialize mock analyzer."""
        self._connected = True

    def connect(self) -> bool:
        """Always returns True."""
        logger.info("Using mock analyzer (no Bedrock connection)")
        return True

    def analyze_resource(self, resource: K8sResource, untracked: UntrackedMoney) -> Optional[AIRecommendation]:
        """Return mock recommendation based on resource name."""
        # Simple heuristic-based recommendations
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

        return AIRecommendation(
            suggested_cost_center=cost_center,
            suggested_owner=owner,
            suggested_tags={
                'cost-center': cost_center,
                'owner': owner,
                'environment': 'prod',
                'application': resource.name,
                'tier': 'backend'
            },
            priority=priority,
            reasoning=f"Based on resource name '{resource.name}', this appears to be part of the {cost_center} system.",
            estimated_savings=untracked.untracked_amount
        )

    def analyze_batch(self, violations: List[tuple]) -> Dict[str, Any]:
        """Analyze multiple violations."""
        results = []
        total_savings = 0.0

        for resource, untracked in violations:
            recommendation = self.analyze_resource(resource, untracked)
            if recommendation:
                results.append({
                    'resource': f"{resource.namespace}/{resource.name}",
                    'kind': resource.kind,
                    'current_cost': untracked.monthly_cost,
                    'untracked_amount': untracked.untracked_amount,
                    'suggestion': {
                        'cost_center': recommendation.suggested_cost_center,
                        'owner': recommendation.suggested_owner,
                        'tags': recommendation.suggested_tags,
                        'priority': recommendation.priority,
                        'reasoning': recommendation.reasoning,
                        'estimated_savings': recommendation.estimated_savings
                    }
                })
                total_savings += recommendation.estimated_savings

        return {
            'analyzed_count': len(violations),
            'recommendations': results,
            'total_estimated_savings': round(total_savings, 2)
        }

    def generate_summary_report(self, untracked_analysis: Dict[str, Any]) -> str:
        """Generate summary report."""
        report = f"""# FinOps Analysis Report (Mock Mode)

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
- **Missing Tags**: {', '.join(v['missing_tags']) if v['missing_tags'] else 'None'}
- **Reason**: {v['reason']}

"""

        return report
