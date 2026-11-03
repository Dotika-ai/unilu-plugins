# ai-dev-factory-spec

Stage 1 (Spec) of the AI Dev Factory, Université du Luxembourg × Dotika.

## Two starting points, one PRD structure

| Case | Example | Flow |
|---|---|---|
| A · existing product (brownfield) | ACME Admission | `/elicitation` → `/opportunity-mapping` → `prd-griller` |
| B · new application (greenfield) | Student App | `/scope-map` → `/scope-challenge` → `/prd-draft` → `prd-griller` (`/opportunity-mapping` optional) |

## What it contains
| Component | Name | Role |
|---|---|---|
| Skill | `/elicitation` | Case A. Restates the existing documentation, asks functional questions one at a time, writes PRD v0.1 |
| Skill | `/scope-map` | Case B. Collects the room's ideas, asks up to 5 questions, proposes a scope map and redraws it live |
| Skill | `/scope-challenge` | Case B. Challenges the scope one point at a time (MVP size, forgotten cases, dependencies, overlap, success), redraws it |
| Skill | `/prd-draft` | Case B. Turns the agreed scope map into PRD v0.1, asks up to 8 business-rule questions |
| Skill | `/opportunity-mapping` | Proposes new features one at a time (accept, reject, park), produces PRD v0.2 |
| Skill | `diagram` | Used by the others. JSON model → clean Excalidraw (grid, straight arrows) + SVG + PNG. Scope maps and process maps |
| Subagent | `prd-griller` | Reviews the PRD in the background: gaps, contradictions, edge cases, testability, MVP discipline (case B) |

## PRD structure (same for both cases)
1. Vision & scope · 2. User types · 3. Business objects · 4. User stories · 5. Acceptance criteria (Gherkin) · 6. Constraints · 7. Glossary · 8. Decisions log

## What it expects around it
- A Claude project with the mission instructions (valid for every stage, not part of this plugin). Case A: with the table of contents of the source documents
- The PRD is a Claude Doc (v0.1, v0.2, v1.0) with its Decisions log inside, exported at each version to Word (for the team) and Markdown (for the agents)
- Code execution turned on in Claude (the diagram skill runs a small Python script, standard library only)
- Connectors turned on in Claude: Granola (meeting notes), Microsoft 365 / Outlook (draft email), Excalidraw (optional, shows the diagrams inline)

## Not yet
Hooks: they come with the Dev stage.
