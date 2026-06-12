"""Simple tag checker for FinOps agent."""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class SimpleTagChecker:
    """Checks if Kubernetes resources have proper FinOps tags."""

    def __init__(self, rules_path: Optional[str] = None):
        """Initialize with tagging rules."""
        self.rules = self._load_rules(rules_path)
        self.required_tags = self.rules.get('required_tags', [])
        self.label_mappings = self.rules.get('label_mappings', {})

    def _load_rules(self, rules_path: Optional[str] = None) -> Dict[str, Any]:
        """Load tagging rules from YAML."""
        if rules_path is None:
            rules_path = Path(__file__).parent.parent / 'config' / 'tagging-rules.yaml'

        try:
            with open(rules_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load tagging rules: {e}")
            return {
                'required_tags': ['owner', 'environment', 'cost-center', 'application', 'tier', 'criticality'],
                'label_mappings': {
                    'owner': ['app.kubernetes.io/owner', 'owner'],
                    'environment': ['app.kubernetes.io/env', 'environment', 'env'],
                    'cost-center': ['app.kubernetes.io/cost-center', 'cost-center', 'costcenter'],
                    'application': ['app.kubernetes.io/name', 'app', 'application'],
                    'tier': ['app.kubernetes.io/tier', 'tier'],
                    'criticality': ['criticality', 'priority', 'severity']
                }
            }

    def _get_tag_value(self, resource: Dict[str, Any], tag: str) -> Optional[str]:
        """Get tag value from resource labels using multiple possible keys."""
        labels = resource.get('labels', {})
        possible_keys = self.label_mappings.get(tag, [tag])
        for key in possible_keys:
            if key in labels:
                return labels[key]
        return None

    def check_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single resource for proper tagging."""
        missing_tags = []
        present_tags = {}

        for tag in self.required_tags:
            value = self._get_tag_value(resource, tag)
            if value:
                present_tags[tag] = value
            else:
                missing_tags.append(tag)

        is_compliant = len(missing_tags) == 0

        category = "properly_tagged"
        if resource.get('is_orphaned'):
            category = "orphaned"
        elif not is_compliant:
            category = "missing_tags"

        return {
            'resource': f"{resource['namespace']}/{resource['name']}",
            'kind': resource['kind'],
            'is_compliant': is_compliant,
            'category': category,
            'missing_tags': missing_tags,
            'present_tags': present_tags,
            'reason': self._get_reason(resource, missing_tags, category)
        }

    def _get_reason(self, resource: Dict[str, Any], missing_tags: List[str], category: str) -> str:
        """Get human-readable reason for compliance status."""
        if category == "orphaned":
            size_gb = resource.get('size_gb', 0)
            return f"Orphaned PVC - {size_gb}GB storage not mounted by any pod"

        if category == "missing_tags":
            return f"Missing required tags: {', '.join(missing_tags)}"

        return "All required tags present - properly tracked"

    def check_all(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check all resources and return summary."""
        results = []
        compliant_count = 0
        non_compliant_count = 0
        orphaned_count = 0

        for resource in resources:
            check_result = self.check_resource(resource)
            results.append(check_result)

            if check_result['is_compliant']:
                compliant_count += 1
            else:
                non_compliant_count += 1
                if check_result['category'] == "orphaned":
                    orphaned_count += 1

        total = len(resources)
        compliant_pct = (compliant_count / total * 100) if total > 0 else 0

        return {
            'total_resources': total,
            'compliant_count': compliant_count,
            'non_compliant_count': non_compliant_count,
            'orphaned_count': orphaned_count,
            'compliant_percentage': round(compliant_pct, 1),
            'results': results
        }

    def print_report(self, analysis: Dict[str, Any]) -> None:
        """Print simple report to console."""
        print("\n" + "=" * 60)
        print("FINOPS TAGGING COMPLIANCE REPORT")
        print("=" * 60)

        print(f"\nTotal Resources Scanned: {analysis['total_resources']}")
        print(f"Compliant Resources: {analysis['compliant_count']} ({analysis['compliant_percentage']}%)")
        print(f"Non-Compliant Resources: {analysis['non_compliant_count']}")
        print(f"Orphaned PVCs: {analysis['orphaned_count']}")

        print("\n" + "-" * 60)
        print("COMPLIANT RESOURCES")
        print("-" * 60)

        compliant = [r for r in analysis['results'] if r['is_compliant']]
        if compliant:
            for r in compliant:
                print(f"✓ {r['resource']} ({r['kind']})")
                print(f"  Tags: {r['present_tags']}")
        else:
            print("None")

        print("\n" + "-" * 60)
        print("NON-COMPLIANT RESOURCES")
        print("-" * 60)

        non_compliant = [r for r in analysis['results'] if not r['is_compliant']]
        if non_compliant:
            for r in non_compliant:
                print(f"✗ {r['resource']} ({r['kind']})")
                print(f"  Missing: {r['missing_tags']}")
                print(f"  Reason: {r['reason']}")
        else:
            print("None - Great job!")

        print("\n" + "=" * 60 + "\n")