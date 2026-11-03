---
name: scope-challenge
description: This skill should be used after /scope-map in a greenfield project, when the team asks to "challenge the scope", "stress-test the MVP", "what did we forget", "is the MVP too big" or calls /scope-challenge. It challenges the agreed scope map one point at a time (MVP size, forgotten users and cases, dependencies on other systems, overlap with what exists, success measures, ideas from other universities), the team decides, and the scope map is redrawn as v<n+1>.
---

# Scope challenge · stress-test the scope before writing the PRD

Goal: a scope the team can defend. In a greenfield project the main risk is a scope that never stops growing, and the second one is an MVP that depends on things nobody controls.
Same rhythm as /opportunity-mapping (one point at a time, the team decides), but the direction is different: here we cut, secure and complete before adding.

## Step 1 · Prepare the challenges
Read the latest scope map model (`scope-map-v*.json`, highest version) and `scope-decisions.md`. Everything already decided there is known: do not reopen it unless a new fact contradicts it.
Generate challenges in 6 families:
1. **MVP size**: an MVP feature that is not needed on day one, or that could start smaller (a link instead of a screen, read-only before self-service, one faculty before all)
2. **Forgotten users and cases**: a user type or situation not on the map (incoming or international students, part-time students, accessibility, the three languages, first use, a lost password, the September peak, a student who leaves)
3. **Dependencies**: an MVP feature that relies on a system marked to confirm, or on data nobody owns. Who owns the data, is it available, what if it is not
4. **Overlap**: a feature that already exists on the website, in ACME, on Moodle or in another app. Replace it, link to it, or leave it out
5. **Success**: how we will know the MVP works, one measurable signal per capability area (for example "share of certificate requests made in the app")
6. **Ideas from other universities**: at most 3 good practices worth considering. They go to Phase 2 or Later by default; the MVP only grows if the room insists
For each challenge: title · what is at stake · proposal (cut, move to Phase 2, add, confirm, link) · impact on the MVP (smaller, same, bigger).
Keep 6 to 12 challenges. Drop anything already in the scope map or in the decisions.

## Step 2 · Present one at a time
Start with the challenges that make the MVP smaller or safer. Format:
C3/10 · **title** · what is at stake (2 lines) · proposal (1 line) · Accept, Reject or Park?
Accept "skip" or "stop" at any time. After each answer, one line to acknowledge, then the next challenge.
Stay functional. No technical design.

## Step 3 · Redraw and log
- Apply every accepted proposal to the model: phase changes, new or removed features, users, systems, out-of-scope items
- Rejected: log it with the reason. Parked: log it with an owner
- Save as the next version (`scope-map-v<n+1>.json`), subtitle `v<n+1> · <date> · after challenge`, and redraw with the **diagram** skill
- Show a short "What changed" list: MVP before and after (number of features), what moved, what was added, what is still to confirm
- Append every decision to `scope-decisions.md`
- End with: "Next: /prd-draft to write PRD v0.1 from this scope map."
