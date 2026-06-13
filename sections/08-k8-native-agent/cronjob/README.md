# CronJob

Scheduled and manual execution resources for the Section 08 agent.

## Files
- `cronjob.yaml` — runs the agent on a schedule (default: hourly)
- `manual-job.yaml` — one-off Job for testing or demos

## Usage
After creating the Secret and applying the manifests:

```bash
kubectl apply -f cronjob.yaml
kubectl create job --from=cronjob/finops-agent finops-agent-demo-run -n finops-agent
kubectl logs -n finops-agent job/finops-agent-demo-run
```

## Notes
- Both resources use `envFrom` to inject the ConfigMap and Secret as environment variables.
- The pod uses `serviceAccountName: finops-agent` so it can read cluster resources.
- Update `image: finops-agent:latest` if you push the image to a registry.
