# Section 03 Goal: Reveal the Problem

## Goal
Show why the cluster is hard to govern at scale by surfacing missing tags, inconsistent ownership, and orphaned resources.

## Prerequisites
Complete Sections 01 and 02.

## Video structure (5 videos)
| Video | Focus | Time |
|-------|------------|-------|------|
| **1** | Why YAML for tagging policy (not JSON) | 2 min |
| **2** | Tagging rules at a glance — keys and values | 2 min |
| **3** | Missing owner/cost-center; billing blind spots | 3–4 min |
| **4** | PVCs with no pods; idle burn | 3–4 min |
| **5** | Escalation pain; why grep does not scale | 3–4 min |

Transcripts: `transcript/1.md` … `transcript/5.md`

## Scope
- Compare well-tagged and poorly tagged workloads
- Demonstrate missing tags/labels/annotations
- Highlight orphaned or unused resources
- Show where ownership is unclear
- Frame the FinOps and operational pain

## Out of scope
- Agent implementation
- Bedrock reasoning
- Issue creation

## Success criteria
The learner can identify at least one good workload, one bad workload, one orphaned resource, and one untracked resource that should later become a tech-debt item.
