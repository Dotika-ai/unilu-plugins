# ai-dev-factory-spec

Stage 1 (Spec) of the AI Dev Factory, Université du Luxembourg × Dotika.

## What it contains
| Component | Name | Role |
|---|---|---|
| Skill | `/elicitation` | Restates the existing documentation, asks functional questions one at a time, writes PRD v0.1 |
| Skill | `/opportunity-mapping` | Proposes new features one at a time (accept, reject, park), produces PRD v0.2 |
| Subagent | `prd-griller` | Reviews the PRD in the background: gaps, contradictions, edge cases, testability |

## PRD structure (set by /elicitation)
1. Vision & scope · 2. User types · 3. Business objects · 4. User stories · 5. Acceptance criteria (Gherkin) · 6. Constraints · 7. Glossary · 8. Decisions log

## What it expects around it
- A Claude project with the mission instructions, including the table of contents of the source documents (valid for every stage, not part of this plugin)
- The PRD is a Claude Doc (v0.1, v0.2, v1.0) with its Decisions log inside, exported at each version to Word (for the team) and Markdown (for the agents)
- Connectors turned on in Claude: Granola (meeting notes) and Microsoft 365 / Outlook (draft email)

## Not yet
Hooks: they come with the Dev stage.
