"""Tagging violation detection for FinOps agent."""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

import yaml

from agent.scanner import K8sResource

logger = logging.getLogger(__name__)


class ViolationCategory(Enum):
    """Categories of tagging violations."""
    UNALLOCATED = "unallocated"      # Missing cost-center
    ORPHANED = "orphaned"            # Resources not actively used
    UNOWNED = "unowned"              # Has cost-center but no owner
    UNKNOWN = "unknown"              # In default namespace with minimal labels
    PROPERLY_TAGGED = "tagged"       # All tags present


@dataclass
class TaggingViolation:
    """Represents a tagging violation for a resource."""
    resource: K8sResource
    category: ViolationCategory
    missing_tags: List[str]
    reason: str


class TaggingViolationDetector:
    """Detects tagging violations in Kubernetes resources."""

    def __init__(self, rules_path: Optional[str] = None):
        """Initialize with tagging rules."""
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

    def analyze_resource(self, resource: K8sResource) -> TaggingViolation:
        """Analyze a single resource for tagging violations."""

        # Check for orphaned PVC
        if resource.kind == "PersistentVolumeClaim" and resource.is_orphaned:
            return TaggingViolation(
                resource=resource,
                category=ViolationCategory.ORPHANED,
                missing_tags=[],
                reason=f"PVC not mounted by any pod - {resource.pvc_size_gb}GB storage is wasted"
            )

        # Check for missing cost-center (unallocated)
        if not self._has_tag(resource, 'cost-center'):
            missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
            return TaggingViolation(
                resource=resource,
                category=ViolationCategory.UNALLOCATED,
                missing_tags=missing,
                reason="Missing cost-center tag - cannot bill to any team"
            )

        # Check for resources in default namespace with no labels
        if resource.namespace == "default" and not resource.labels:
            missing = self.required_tags.copy()
            return TaggingViolation(
                resource=resource,
                category=ViolationCategory.UNKNOWN,
                missing_tags=missing,
                reason="Resource in default namespace with no labels - likely untracked"
            )

        # Check for missing owner (unowned but has cost-center)
        if not self._has_tag(resource, 'owner'):
            missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
            return TaggingViolation(
                resource=resource,
                category=ViolationCategory.UNOWNED,
                missing_tags=missing,
                reason="Has cost-center but missing owner - no accountability"
            )

        # Check for other missing tags
        missing = [tag for tag in self.required_tags if not self._has_tag(resource, tag)]
        if missing:
            return TaggingViolation(
                resource=resource,
                category=ViolationCategory.UNOWNED,
                missing_tags=missing,
                reason=f"Missing tags: {', '.join(missing)}"
            )

        # All tags present - properly tagged
        return TaggingViolation(
            resource=resource,
            category=ViolationCategory.PROPERLY_TAGGED,
            missing_tags=[],
            reason="All required tags present - properly tagged"
        )

    def analyze_all(self, resources: List[K8sResource]) -> Dict[str, Any]:
        """Analyze all resources and return summary."""
        results = []
        category_counts = {cat: 0 for cat in ViolationCategory}

        for resource in resources:
            analysis = self.analyze_resource(resource)
            results.append(analysis)
            category_counts[analysis.category] += 1

        total_resources = len(results)
        violation_count = sum(
            1 for r in results
            if r.category != ViolationCategory.PROPERLY_TAGGED
        )
        properly_tagged_count = total_resources - violation_count

        return {
            'total_resources': total_resources,
            'properly_tagged': properly_tagged_count,
            'violations': violation_count,
            'tagged_percentage': round((properly_tagged_count / total_resources * 100) if total_resources > 0 else 0, 1),
            'violation_percentage': round((violation_count / total_resources * 100) if total_resources > 0 else 0, 1),
            'breakdown_by_category': {
                cat.value: count
                for cat, count in category_counts.items()
                if count > 0
            },
            'violations_list': [
                {
                    'resource': f"{r.resource.namespace}/{r.resource.name}",
                    'kind': r.resource.kind,
                    'category': r.category.value,
                    'missing_tags': r.missing_tags,
                    'reason': r.reason
                }
                for r in results
                if r.category != ViolationCategory.PROPERLY_TAGGED
            ],
            'properly_tagged_list': [
                {
                    'resource': f"{r.resource.namespace}/{r.resource.name}",
                    'kind': r.resource.kind
                }
                for r in results
                if r.category == ViolationCategory.PROPERLY_TAGGED
            ]
        }

    def get_violations(self, resources: List[K8sResource]) -> List[TaggingViolation]:
        """Get all tagging violations."""
        violations = []
        for resource in resources:
            analysis = self.analyze_resource(resource)
            if analysis.category != ViolationCategory.PROPERLY_TAGGED:
                violations.append(analysis)

        return violations