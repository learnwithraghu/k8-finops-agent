# Infographic & Metaphor Thinking Skill

**Skill ID:** `infographic-metaphor`

**Purpose:**
Provide a structured approach to designing visual infographics and metaphor‑based explanations for complex technical concepts. This skill can be invoked from other skills (e.g., `create-presentation-svgs.md`) to generate consistent, high‑impact visual assets.

**Key Steps**
1. **Clarify the Core Message** – Define the single sentence that captures the concept.
2. **Select a Metaphor** – Choose a relatable analogy (e.g., "bridge", "pipeline", "maze").
3. **Map Elements to Visual Tokens** – Identify reusable SVG icons (cluster, JSON, brain, Python agent, etc.) and palette colors.
4. **Design Layout** – Decide on a 16:9 canvas, split‑screen or layered flow, and placement of titles, icons, arrows.
5. **Generate SVG Snippets** – Use the SVG generator (or embed existing `<defs>` icons) to create each component.
6. **Assemble & Export** – Combine the snippets into a final SVG file and optionally produce a Markdown guide.

**Parameters**
- `title` – Short slide title (max 6‑8 words).
- `metaphor` – Chosen metaphor term (e.g., "bridge", "pipeline", "maze").
- `components` – List of visual components to include (e.g., `cluster`, `json`, `python-agent`).
- `palette` – Optional custom color palette; defaults to AWS/GCP style.

**Example Usage** (in another skill):
```markdown
{{% call_skill "infographic-metaphor" 
   title="Connecting K8s Metadata to FinOps" 
   metaphor="bridge" 
   components=["cluster","json","python-agent"] 
   palette="aws" 
%}}
```
The skill will output a Markdown block with a description of the visual layout and a reference to the generated SVG file (e.g., `slides/bridge_k8s_finops.svg`).

**Outputs**
- `description.md` – Short narrative explaining the infographic.
- `slide.svg` – Final SVG ready for inclusion in the presentation.

**Integration Tips**
- Store generated SVGs under `sections/04-local-python-agent/slides/`.
- The repository already has a `skills` symlink pointing to `.kilo/skills/`.
- Update `create-presentation-svgs.md` to call this skill whenever a metaphor‑driven slide is needed.

---
*This skill file is concise for quick reference. Extend or adapt as your visual design needs evolve.*
