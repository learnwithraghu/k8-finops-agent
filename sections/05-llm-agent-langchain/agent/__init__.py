"""K8s FinOps Agent - AI-powered cost optimization for Kubernetes."""

__version__ = "1.0.0"
__author__ = "FinOps Team"

from agent.scanner import K8sScanner, K8sResource
from agent.tagging_violations import TaggingViolationDetector, TaggingViolation
from agent.analyzer import IssueDraft

__all__ = [
    'K8sScanner',
    'K8sResource',
    'TaggingViolationDetector',
    'TaggingViolation',
    'IssueDraft',
]
