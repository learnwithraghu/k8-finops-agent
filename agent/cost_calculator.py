"""Cost calculation engine for FinOps agent."""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

import yaml

from agent.scanner import K8sResource

logger = logging.getLogger(__name__)


@dataclass
class CostBreakdown:
    """Cost breakdown for a resource."""
    monthly_compute: float = 0.0
    monthly_storage: float = 0.0
    monthly_total: float = 0.0
    hourly_rate: float = 0.0


class CostCalculator:
    """Calculates costs for Kubernetes resources based on EC2 pricing."""

    def __init__(self, pricing_config_path: Optional[str] = None):
        """Initialize with pricing configuration."""
        self.pricing = self._load_pricing(pricing_config_path)
        self.instance_hourly = self.pricing['ec2']['t2.medium']['hourly_usd']
        self.total_millicores = self.pricing['constants']['total_millicores']
        self.hours_per_month = self.pricing['constants']['hours_per_month']
        self.storage_price_gb = self.pricing['storage']['gp3']['gb_per_month_usd']

    def _load_pricing(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load pricing configuration from YAML."""
        if config_path is None:
            # Look in config directory relative to project root
            config_path = Path(__file__).parent.parent / 'config' / 'pricing.yaml'

        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load pricing config from {config_path}: {e}")
            # Return default pricing for t2.medium
            return {
                'ec2': {
                    't2.medium': {
                        'hourly_usd': 0.0464,
                        'vcpu': 2,
                        'memory_gb': 4
                    }
                },
                'storage': {
                    'gp3': {'gb_per_month_usd': 0.08}
                },
                'constants': {
                    'hours_per_month': 730,
                    'total_millicores': 2000
                }
            }

    def calculate_resource_cost(self, resource: K8sResource) -> CostBreakdown:
        """Calculate monthly cost for a Kubernetes resource."""
        breakdown = CostBreakdown()

        # Calculate compute cost based on CPU request
        if resource.cpu_request > 0:
            # Fraction of total cluster CPU
            cpu_fraction = resource.cpu_request / self.total_millicores
            # Hourly cost for this resource
            hourly_cost = self.instance_hourly * cpu_fraction * resource.replicas
            # Monthly compute cost
            breakdown.monthly_compute = hourly_cost * self.hours_per_month
            breakdown.hourly_rate = hourly_cost

        # Calculate storage cost
        if resource.pvc_size_gb > 0:
            breakdown.monthly_storage = resource.pvc_size_gb * self.storage_price_gb

        # Total cost
        breakdown.monthly_total = breakdown.monthly_compute + breakdown.monthly_storage

        return breakdown

    def calculate_cluster_cost(self, resources: list) -> Dict[str, Any]:
        """Calculate total cost for all resources in cluster."""
        total_compute = 0.0
        total_storage = 0.0
        resource_costs = []

        for resource in resources:
            cost = self.calculate_resource_cost(resource)
            total_compute += cost.monthly_compute
            total_storage += cost.monthly_storage

            resource_costs.append({
                'name': resource.name,
                'namespace': resource.namespace,
                'kind': resource.kind,
                'monthly_cost': round(cost.monthly_total, 2),
                'compute': round(cost.monthly_compute, 2),
                'storage': round(cost.monthly_storage, 2)
            })

        return {
            'total_monthly': round(total_compute + total_storage, 2),
            'total_compute': round(total_compute, 2),
            'total_storage': round(total_storage, 2),
            'resources': resource_costs
        }

    def get_instance_specs(self) -> Dict[str, Any]:
        """Get EC2 instance specifications."""
        return self.pricing['ec2']['t2.medium']
