"""GitHub client for creating FinOps issues."""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from github import Github
from github.GithubException import GithubException

from agent.scanner import K8sResource
from agent.untracked_money import UntrackedMoney
from agent.analyzer import AIRecommendation

logger = logging.getLogger(__name__)


class GitHubIssueClient:
    """Creates GitHub issues for FinOps violations."""

    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        """Initialize GitHub client."""
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo_name = repo_name or os.getenv('GITHUB_REPO')
        self.github = None
        self.repo = None
        self._connected = False

    def connect(self) -> bool:
        """Connect to GitHub API."""
        if not self.token:
            logger.error("GitHub token not provided")
            return False
        if not self.repo_name:
            logger.error("GitHub repo not provided")
            return False

        try:
            self.github = Github(self.token)
            self.repo = self.github.get_repo(self.repo_name)
            self._connected = True
            logger.info(f"Connected to GitHub repo: {self.repo_name}")
            return True
        except GithubException as e:
            logger.error(f"Failed to connect to GitHub: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to GitHub: {e}")
            return False

    def _generate_issue_title(self, resource: K8sResource, untracked: UntrackedMoney) -> str:
        """Generate issue title."""
        return f"[FinOps] {resource.namespace}/{resource.name} - {untracked.category.value.upper()} (${untracked.untracked_amount:.2f}/month)"

    def _generate_issue_body(
        self,
        resource: K8sResource,
        untracked: UntrackedMoney,
        recommendation: Optional[AIRecommendation] = None
    ) -> str:
        """Generate detailed issue body."""
        body = f"""## Resource Details

| Field | Value |
|-------|-------|
| **Name** | {resource.name} |
| **Namespace** | {resource.namespace} |
| **Kind** | {resource.kind} |
| **Monthly Cost** | ${untracked.monthly_cost:.2f} |
| **Untracked Amount** | ${untracked.untracked_amount:.2f} |
| **Category** | {untracked.category.value} |

## Current Labels

```yaml
{self._format_labels(resource.labels)}
```

## Issue

{untracked.reason}

## Missing Tags

{self._format_missing_tags(untracked.missing_tags)}

## Cost Impact

- **Monthly Cost**: ${untracked.monthly_cost:.2f}
- **Untracked**: ${untracked.untracked_amount:.2f}
- **Percentage Untracked**: {(untracked.untracked_amount / untracked.monthly_cost * 100) if untracked.monthly_cost > 0 else 0:.1f}%

"""

        if recommendation:
            body += f"""## AI Recommendation

### Suggested Tags

| Tag | Current | Suggested |
|-----|---------|-----------|
| cost-center | {resource.labels.get('cost-center', resource.labels.get('app.kubernetes.io/cost-center', 'N/A'))} | **{recommendation.suggested_cost_center}** |
| owner | {resource.labels.get('owner', resource.labels.get('app.kubernetes.io/owner', 'N/A'))} | **{recommendation.suggested_owner}** |

### Full Tag Set

```yaml
{self._format_labels(recommendation.suggested_tags)}
```

### Reasoning

{recommendation.reasoning}

### Estimated Savings

By properly tagging this resource, you can track **${untracked.untracked_amount:.2f}/month** of currently untracked costs.

**Priority**: {recommendation.priority.upper()}

"""

        body += f"""## Remediation Steps

1. Add the missing tags to the resource:
   ```bash
   kubectl label {resource.kind.lower()} {resource.name} -n {resource.namespace} \\
     cost-center={recommendation.suggested_cost_center if recommendation else 'YOUR_COST_CENTER'} \\
     owner={recommendation.suggested_owner if recommendation else 'YOUR_TEAM'}
   ```

2. Update the resource manifest to include these labels permanently.

3. Verify the labels are applied:
   ```bash
   kubectl get {resource.kind.lower()} {resource.name} -n {resource.namespace} --show-labels
   ```

## Additional Information

- **Detected At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Agent Version**: v1.0.0
- **Instance Type**: t2.medium

---
*This issue was automatically created by the K8s FinOps Agent.*
"""

        return body

    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Format labels as YAML."""
        if not labels:
            return "# No labels"
        lines = []
        for key, value in sorted(labels.items()):
            lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def _format_missing_tags(self, missing_tags: List[str]) -> str:
        """Format missing tags as list."""
        if not missing_tags:
            return "- None"
        return "\n".join(f"- [ ] `{tag}`" for tag in missing_tags)

    def _get_labels(self, untracked: UntrackedMoney, recommendation: Optional[AIRecommendation] = None) -> List[str]:
        """Generate labels for the issue."""
        labels = [
            "finops",
            f"category:{untracked.category.value}",
            f"kind:{untracked.resource.kind.lower()}"
        ]

        if recommendation:
            labels.append(f"priority:{recommendation.priority}")

        # Add cost-based labels
        if untracked.untracked_amount > 50:
            labels.append("cost:critical")
        elif untracked.untracked_amount > 20:
            labels.append("cost:high")
        elif untracked.untracked_amount > 5:
            labels.append("cost:medium")
        else:
            labels.append("cost:low")

        return labels

    def _check_existing_issue(self, resource: K8sResource) -> Optional[Any]:
        """Check if an issue already exists for this resource."""
        try:
            # Search for open issues with similar title
            title_pattern = f"[FinOps] {resource.namespace}/{resource.name}"
            issues = self.repo.get_issues(state='open')

            for issue in issues:
                if title_pattern in issue.title:
                    logger.info(f"Found existing issue #{issue.number} for {resource.name}")
                    return issue

            return None
        except GithubException as e:
            logger.error(f"Error checking existing issues: {e}")
            return None

    def create_issue(
        self,
        resource: K8sResource,
        untracked: UntrackedMoney,
        recommendation: Optional[AIRecommendation] = None,
        dry_run: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Create a GitHub issue for a violation."""
        if not self._connected:
            logger.error("GitHub client not connected")
            return None

        # Check for existing issue
        existing = self._check_existing_issue(resource)
        if existing:
            logger.info(f"Skipping duplicate issue for {resource.name}")
            return {
                'issue_number': existing.number,
                'url': existing.html_url,
                'status': 'duplicate'
            }

        title = self._generate_issue_title(resource, untracked)
        body = self._generate_issue_body(resource, untracked, recommendation)
        labels = self._get_labels(untracked, recommendation)

        if dry_run:
            logger.info(f"[DRY RUN] Would create issue: {title}")
            return {
                'title': title,
                'labels': labels,
                'status': 'dry_run'
            }

        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            logger.info(f"Created issue #{issue.number}: {title}")
            return {
                'issue_number': issue.number,
                'url': issue.html_url,
                'title': title,
                'labels': labels,
                'status': 'created'
            }
        except GithubException as e:
            logger.error(f"Failed to create issue: {e}")
            return None

    def create_issues_batch(
        self,
        violations: List[tuple],
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Create issues for multiple violations."""
        results = {
            'created': [],
            'duplicates': [],
            'failed': [],
            'total': len(violations)
        }

        for resource, untracked, recommendation in violations:
            result = self.create_issue(resource, untracked, recommendation, dry_run)
            if result:
                if result.get('status') == 'created':
                    results['created'].append(result)
                elif result.get('status') == 'duplicate':
                    results['duplicates'].append(result)
                elif result.get('status') == 'dry_run':
                    results['created'].append(result)  # Count as created in dry run
            else:
                results['failed'].append({
                    'resource': f"{resource.namespace}/{resource.name}",
                    'error': 'Failed to create issue'
                })

        return results


class MockGitHubClient:
    """Mock GitHub client for testing without actual GitHub access."""

    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        """Initialize mock client."""
        self.token = token or "mock-token"
        self.repo_name = repo_name or "mock-org/mock-repo"
        self._connected = False
        self._issues = []

    def connect(self) -> bool:
        """Always returns True."""
        self._connected = True
        logger.info(f"[MOCK] Connected to GitHub repo: {self.repo_name}")
        return True

    def create_issue(
        self,
        resource,
        untracked,
        recommendation=None,
        dry_run=False
    ) -> Optional[Dict[str, Any]]:
        """Mock create issue - just logs."""
        if not self._connected:
            logger.error("Mock GitHub client not connected")
            return None

        title = f"[FinOps] {resource.namespace}/{resource.name} - {untracked.category.value.upper()}"

        logger.info(f"[MOCK] Would create issue: {title}")
        logger.info(f"[MOCK]   - Monthly Cost: ${untracked.monthly_cost:.2f}")
        logger.info(f"[MOCK]   - Untracked: ${untracked.untracked_amount:.2f}")
        if recommendation:
            logger.info(f"[MOCK]   - Suggested cost-center: {recommendation.suggested_cost_center}")
            logger.info(f"[MOCK]   - Suggested owner: {recommendation.suggested_owner}")

        return {
            'issue_number': len(self._issues) + 1,
            'url': f"https://github.com/{self.repo_name}/issues/{len(self._issues) + 1}",
            'title': title,
            'status': 'mock_created'
        }

    def create_issues_batch(self, violations, dry_run=False) -> Dict[str, Any]:
        """Mock batch create."""
        results = {
            'created': [],
            'duplicates': [],
            'failed': [],
            'total': len(violations)
        }

        for resource, untracked, recommendation in violations:
            result = self.create_issue(resource, untracked, recommendation, dry_run)
            if result:
                results['created'].append(result)

        return results
