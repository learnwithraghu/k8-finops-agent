"""Untracked money detection for FinOps agent."""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

import yaml

from agent.scanner import K8sResource
from agent.cost_calculator import CostCalculator, CostBreakdown

logger = logging.getLogger(__name__)


class UntrackedCategory(Enum):
    """Categories of untracked money."""
    UNALLOCATED = "unallocated"      # Missing cost-center
    ORPHANED = "orphaned"            # Resources not actively used
    UNOWNED = "unowned"              # Has cost-center but no owner
    UNKNOWN = "unknown"              # In default namespace with minimal labels
    PROPERLY_TRACKED = "tracked"     # All tags present


@dataclass
class UntrackedMoney:
    """Represents untracked money for a resource."""
    resource: K8sResource
    category: UntrackedCategory
    monthly_cost: float
    untracked_amount: float
    missing_tags: List[str]
    reason: str


class UntrackedMoneyDetector:
    """Detects untracked money in Kubernetes resources."""

    def __init__(self, calculator: CostCalculator, rules_path: Optional[str] = None):
        """Initialize with cost calculator and tagging rules."""
        self.calculator = calculator
        self.rules = self._load_rules(rules_path)
        self.required_tags = self.rules.get('required_tags', [])
        self.label_mappings = self.rules.get('label_mappings', {})

    def _load_rules(self, rules_path: Optional[str] = None) -> Dict[str, Any]:
        """Load tagging rules from YAML."""
        if rules_path is None:
            from pathlib import Path
            rules_path = Path(__file__).parent.parent / 'config' / 'tagging-rules.yaml'

        try:
            with open(rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load tagging rules: {e}")
            return {
                'required_tags': ['owner', 'environment', 'cost-center', 'application', 'tier'],
                'label_mappings': {
                    'owner': ['app.kubernetes.io/owner', 'owner'],
                    'environment': ['app.kubernetes.io/env', 'environment', 'env'],
                    'cost-center': ['app.kubernetes.io/cost-center', 'cost-center', 'costcenter'],
                    'application': ['app.kubernetes.io/name', 'app', 'application'],
                    'tier': ['app.kubernetes.io/tier', 'tier']
                }
            }

    def _get_tag_value(self, resource: K8sResource, tag: str) -> Optional[str]:
        """Get tag value from resource labels using multiple possible keys."""
        possible_keys = self.label_mappings.get(tag, [tag])
        for key in possible_keys:
            if key in resource.labels:
                return resource.labels[key]
        return None

    def _has_tag(self, resource: K8sResource, tag: str) -> bool:
        """Check if resource has a specific tag."""
        return self._get_tag_value(resource, tag) is not None

    def analyze_resource(self, resource: K8sResource) -> UntrackedMoney:
        """Analyze a single resource for untracked money."""
        cost = self.calculator.calculate_resource_cost(resource)
        monthly_cost = cost.monthly_total

        # Check for orphaned PVC
        if resource.kind == "PersistentVolumeClaim" and resource.is_orphaned:
            return UntrackedMoney(
                resource=resource,
                category=UntrackedCategory.ORPHANED,
                monthly_cost=monthly_cost,
                untracked_amount=monthly_cost,  # 100% waste
                missing_tags=[],
                reason=f"PVC not mounted by any pod - {resource.pvc_size_gb}GB storage is wasted"
            )

        # Check for missing cost-center (unallocated)
        if not self._has_tag(resource, 'cost-center'):
            missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
            return UntrackedMoney(
                resource=resource,
                category=UntrackedCategory.UNALLOCATED,
                monthly_cost=monthly_cost,
                untracked_amount=monthly_cost,  # Full cost is untracked
                missing_tags=missing,
                reason="Missing cost-center tag - cannot bill to any team"
            )

        # Check for resources in default namespace with no labels
        if resource.namespace == "default" and not resource.labels:
            missing = self.required_tags.copy()
            return UntrackedMoney(
                resource=resource,
                category=UntrackedCategory.UNKNOWN,
                monthly_cost=monthly_cost,
                untracked_amount=monthly_cost,
                missing_tags=missing,
                reason="Resource in default namespace with no labels - likely untracked"
            )

        # Check for missing owner (unowned but has cost-center)
        if not self._has_tag(resource, 'owner'):
            missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
            return UntrackedMoney(
                resource=resource,
                category=UntrackedCategory.UNOWNED,
                monthly_cost=monthly_cost,
                untracked_amount=monthly_cost * 0.5,  # Partially tracked
                missing_tags=missing,
                reason="Has cost-center but missing owner - no accountability"
            )

        # Check for other missing tags
        missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
        if missing:
            # Some tags present but not all - partially tracked
            untracked_pct = len(missing) / len(self.required_tags)
            return UntrackedMoney(
                resource=resource,
                category=UntrackedCategory.UNOWNED,
                monthly_cost=monthly_cost,
                untracked_amount=monthly_cost * untracked_pct,
                missing_tags=missing,
                reason=f"Missing tags: {', '.join(missing)}"
            )

        # All tags present - properly tracked
        return UntrackedMoney(
            resource=resource,
            category=UntrackedCategory.PROPERLY_TRACKED,
            monthly_cost=monthly_cost,
            untracked_amount=0.0,
            missing_tags=[],
            reason="All required tags present - properly tracked"
        )

    def analyze_all(self, resources: List[K8sResource]) -> Dict[str, Any]:
        """Analyze all resources and return summary."""
        results = []
        category_totals = {cat: 0.0 for cat in UntrackedCategory}

        for resource in resources:
            analysis = self.analyze_resource(resource)
            results.append(analysis)
            category_totals[analysis.category] += analysis.untracked_amount

        total_cost = sum(r.monthly_cost for r in results)
        total_untracked = sum(r.untracked_amount for r in results)
        tracked_amount = total_cost - total_untracked

        return {
            'total_monthly_cost': round(total_cost, 2),
            'total_tracked': round(tracked_amount, 2),
            'total_untracked': round(total_untracked, 2),
            'tracked_percentage': round((tracked_amount / total_cost * 100) if total_cost > 0 else 0, 1),
            'untracked_percentage': round((total_untracked / total_cost * 100) if total_cost > 0 else 0, 1),
            'breakdown_by_category': {
                cat.value: round(amount, 2)
                for cat, amount in category_totals.items()
                if amount > 0
            },
            'violations': [
                {
                    'resource': f"{r.resource.namespace}/{r.resource.name}",
                    'kind': r.resource.kind,
                    'category': r.category.value,
                    'monthly_cost': round(r.monthly_cost, 2),
                    'untracked_amount': round(r.untracked_amount, 2),
                    'missing_tags': r.missing_tags,
                    'reason': r.reason
                }
                for r in results
                if r.category != UntrackedCategory.PROPERLY_TRACKED
            ],
            'properly_tracked': [
                {
                    'resource': f"{r.resource.namespace}/{r.resource.name}",
                    'kind': r.resource.kind,
                    'monthly_cost': round(r.monthly_cost, 2)
                }
                for r in results
                if r.category == UntrackedCategory.PROPERLY_TRACKED
            ]
        }

    def get_high_impact_violations(self, resources: List[K8sResource], threshold: float = 10.0) -> List[UntrackedMoney]:
        """Get violations with high untracked cost."""
        violations = []
        for resource in resources:
            analysis = self.analyze_resource(resource)
            if analysis.category != UntrackedCategory.PROPERLY_TRACKED:
                if analysis.untracked_amount >= threshold:
                    violations.append(analysis)

        # Sort by untracked amount (highest first)
        violations.sort(key=lambda x: x.untracked_amount, reverse=True)
        return violations
