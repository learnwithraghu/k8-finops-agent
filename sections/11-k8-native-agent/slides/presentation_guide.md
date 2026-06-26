# Slide Presentation Guide: Section 11 Helm-Based Deployment

This guide accompanies the generated SVG slide assets to help you narrate this section before jumping into the live demo.

---

## Slide 1: Goal
*   **File**: [slide1_goal.svg](slide1_goal.svg)
*   **Narrative Focus**:
    *   Explain the evolution: In Section 08, we built an LLM-powered FinOps agent that runs locally. Now we're packaging it for production deployment inside Kubernetes.
    *   Introduce Helm: Instead of managing raw YAML manifests, we use Helm for templating, versioning, and lifecycle management.
    *   Core Goal: Deploy the agent as a scheduled CronJob that runs in-cluster with professional packaging.
    *   Highlight the three key benefits: Templating (reusable configs), Versioning (track changes), and Testing (validate deployments).

---

## Slide 2: Helm Chart Structure
*   **File**: [slide2_helm_structure.svg](slide2_helm_structure.svg)
*   **Narrative Focus**:
    *   Walk through the directory tree: Show that a Helm chart is just a structured collection of files.
    *   Chart.yaml: Metadata about the chart itself (name, version, description).
    *   values.yaml: The configuration hub – all customizable settings live here.
    *   templates/: Where the magic happens – Go templates that generate Kubernetes manifests dynamically.
    *   _helpers.tpl: Reusable template functions for common patterns (labels, names).
    *   NOTES.txt: Post-install instructions that guide users on next steps.
    *   Emphasize: This structure separates configuration from implementation, making the chart reusable across environments.

---

## Slide 3: Key Concepts
*   **File**: [slide3_key_concepts.svg](slide3_key_concepts.svg)
*   **Narrative Focus**:
    *   Break down the four fundamental concepts:
    *   **Templating**: Go template syntax allows dynamic value injection using {{ .Values.key }}. No more hardcoded values.
    *   **ConfigMaps vs Secrets**: ConfigMaps hold non-sensitive data (tagging rules, LLM config). Secrets hold API keys and are managed outside Helm for security.
    *   **In-Cluster Config**: The agent uses a ServiceAccount token instead of kubeconfig. RBAC controls what it can read (read-only ClusterRole).
    *   **Lifecycle Management**: helm install, upgrade, rollback, and test provide a complete deployment workflow with version tracking.

---

## Slide 4: Deployment Workflow
*   **File**: [slide4_deployment_workflow.svg](slide4_deployment_workflow.svg)
*   **Narrative Focus**:
    *   Walk through the 6-step deployment process:
    *   **Step 1**: Build the Docker image with the agent code.
    *   **Step 2**: Load the image into Kind cluster (local development).
    *   **Step 3**: Create the API key Secret manually (security best practice).
    *   **Step 4**: Lint the chart to catch errors before deployment.
    *   **Step 5**: Install the chart with `helm install`.
    *   **Step 6**: Validate with `helm test` to ensure everything works.
    *   Emphasize: This workflow is reproducible and can be automated in CI/CD pipelines.

---

## Slide 5: Configuration Management
*   **File**: [slide5_configuration.svg](slide5_configuration.svg)
*   **Narrative Focus**:
    *   Show how values.yaml centralizes all configuration.
    *   Left side: Example values.yaml with namespace, schedule, resources, and tagging rules.
    *   Right side: Four common customization scenarios:
        1. Change the CronJob schedule (e.g., every 30 minutes instead of hourly).
        2. Add a new required tag to the tagging policy.
        3. Limit scans to a specific namespace (e.g., booking-api).
        4. Increase memory limits for larger clusters.
    *   Key Point: All customizations happen via `helm upgrade --set` or custom values files. No image rebuilds needed.

---

## Slide 6: CronJob Architecture
*   **File**: [slide6_cronjob_architecture.svg](slide6_cronjob_architecture.svg)
*   **Narrative Focus**:
    *   Explain the Kubernetes resource hierarchy:
    *   **CronJob**: Schedules Jobs based on cron syntax (e.g., hourly). Controls concurrency and history limits.
    *   **Job**: Ensures the Pod completes successfully. Handles retries and backoff.
    *   **Pod**: Runs the finops-agent container with 6 steps: load config, read secret, scan cluster, call LLM, generate report, exit.
    *   Show the dependencies: ConfigMap (tagging rules + LLM config), Secret (API key), ServiceAccount (RBAC token).
    *   Emphasize: In-cluster execution means no kubeconfig needed – the pod uses its ServiceAccount token automatically.

---

## Slide 7: Benefits & Best Practices
*   **File**: [slide7_benefits.svg](slide7_benefits.svg)
*   **Narrative Focus**:
    *   Compare Helm to raw manifests:
    *   **Benefits**: Templating, versioning, rollback, testing, customization, documentation.
    *   **Best Practices**: Keep secrets external, use _helpers.tpl for DRY code, version charts independently, document with NOTES.txt, always lint before installing, use dry-run to preview changes.
    *   Key Takeaway: Helm transforms static YAML into maintainable, version-controlled infrastructure-as-code. Configuration changes no longer require rebuilding images.

---

## Slide 8: Next Steps
*   **File**: [slide8_next_steps.svg](slide8_next_steps.svg)
*   **Narrative Focus**:
    *   Recap what learners accomplished:
        - Helm chart structure, Go templates, ConfigMaps vs Secrets, in-cluster config, lifecycle commands, RBAC, CronJob scheduling, helm test.
    *   Preview possible extensions:
        - Integrate with issue tracker (Section 10)
        - Add persistent storage for reports (PVC or S3)
        - Use Sealed Secrets or External Secrets Operator for production
        - Deploy to managed Kubernetes (EKS, GKE, AKS)
        - Add Prometheus metrics and Grafana dashboards
        - Create CI/CD pipelines for automated deployments
        - Set up alerts for compliance thresholds
    *   Congratulate: Section 11 complete! The agent is now production-ready with professional packaging.

---

## Demo Flow Recommendation

After presenting the slides, transition to a live demo:

1. **Show the chart structure**: `tree sections/11-k8-native-agent/helm/`
2. **Inspect values.yaml**: `cat sections/11-k8-native-agent/helm/values.yaml`
3. **Build and load the image**: Show the Docker build and Kind load process
4. **Create the secret**: Demonstrate manual secret creation
5. **Lint the chart**: `helm lint sections/11-k8-native-agent/helm/`
6. **Install the chart**: `helm install finops-agent sections/11-k8-native-agent/helm/`
7. **Run helm test**: `helm test finops-agent` and show the logs
8. **Customize**: Change the schedule with `helm upgrade --set schedule="*/15 * * * *"`
9. **Show history**: `helm history finops-agent`
10. **Rollback**: Demonstrate `helm rollback finops-agent`

This combination of slides + live demo provides a complete learning experience for Helm-based Kubernetes deployments.
