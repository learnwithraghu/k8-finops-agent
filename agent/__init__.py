"""K8s FinOps Agent - AI-powered cost optimization for Kubernetes."""

__version__ = "1.0.0"
__author__ = "FinOps Team"

from agent.scanner import K8sScanner, K8sResource
from agent.cost_calculator import CostCalculator, CostBreakdown
from agent.untracked_money import UntrackedMoneyDetector, UntrackedMoney, UntrackedCategory
from agent.analyzer import BedrockAnalyzer, MockAnalyzer, AIRecommendation
from agent.github_client import GitHubIssueClient, MockGitHubClient

__all__ = [
    'K8sScanner',
    'K8sResource',
    'CostCalculator',
    'CostBreakdown',
    'UntrackedMoneyDetector',
    'UntrackedMoney',
    'UntrackedCategory',
    'BedrockAnalyzer',
    'MockAnalyzer',
    'AIRecommendation',
    'GitHubIssueClient',
    'MockGitHubClient',
]
