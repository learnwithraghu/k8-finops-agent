# Section 04 Goal: FinOps AI Architecture Design

## Goal
Convert the problem from Section 02a (missing ownership labels, manual debugging, no automation) into a concrete architecture for an AI-powered FinOps agent. Students learn to think from problem → tools → flow → components before writing code.

This is a whiteboarding section — no demos, no code. Three videos that walk through the design journey.

## Prerequisites
Complete Sections 01, 02, and 02a first.

You should have experienced:
- Deploying and inspecting workloads with kubectl (Section 02)
- The ownership wall incident — payment API down, no labels, no owner (Section 02a)
- The pain of manual debugging without metadata

## Video structure (3 videos)
| Video | Focus | Time |
|-------|-------|------|
| **1** | The problem we're solving — recap the pain, define the system question | 3 min |
| **2** | The architecture pattern — data flow, tool selection, the pipeline | 3 min |
| **3** | Component design — responsibilities, inputs, outputs, trade-offs | 3 min |

Each video is one clear beat. Students go from "I felt the pain" to "I understand the design" in under 10 minutes.

## Scope
- Recap the Section 02a incident and frame it as a system design problem
- Define the three phases: Collect → Analyze → Act
- Evaluate tool options for each phase (kubectl, Python client, MCP, LLM, REST)
- Draw the full pipeline: Cluster → MCP Server → Collector → LLM → Tracker → Board
- Break down each component's responsibility, inputs, outputs, and trade-offs

## Out of scope
- Writing code (Sections 05+)
- Tool installation or setup
- Kubernetes deployment

## Success criteria
The learner can:
1. Explain why manual kubectl does not scale for FinOps
2. Describe the Collect → Analyze → Act pipeline
3. Justify the choice of MCP, LLM, and a tracker for each phase
4. Draw the architecture from memory
5. Articulate the trade-off for each component choice
