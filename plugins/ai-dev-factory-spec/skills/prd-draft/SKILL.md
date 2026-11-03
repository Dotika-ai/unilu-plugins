---
name: prd-draft
description: This skill should be used in a greenfield project after /scope-map (and usually /scope-challenge), when the team asks to "write the PRD", "turn the scope into a PRD", "draft PRD v0.1" or calls /prd-draft. It turns the agreed scope map and its decisions into PRD v0.1, with the same structure as /elicitation, asking a few business-rule questions one at a time.
---

# PRD draft · from the scope map to PRD v0.1

Goal: PRD v0.1 for a new application, written from what the room agreed, in the same structure as the PRDs written with /elicitation, so that the Design and Dev stages read every PRD the same way.
Sources: the latest scope map model (`scope-map-v*.json`, highest version), `scope-decisions.md`, any process map drawn in the session, and the project instructions. Nothing else is a source: what you add yourself is marked (Assumption).

## Step 1 · Pick the key journeys
From the MVP features, list the 2 to 4 journeys that carry the value (for example "a student requests a certificate and gets it"). Show them in one message and ask the room to confirm or reorder. Wait.
For the first journey (or any journey the room asks for), draw a process map with the **diagram** skill: it makes the business rules and exceptions visible before writing the acceptance criteria.

## Step 2 · Ask the business rules, one question at a time, 8 questions at most
Only what is needed to write testable acceptance criteria for the MVP. Format: Q2/8 · the question · why it matters (1 line) · best guess.
Ask about rules and exceptions: who may do it, when, what is checked, what if it fails, what the user sees, deadlines, languages, how long data is kept.
Prefer closed questions and concrete examples ("a part-time student asking for a certificate in German"). Accept "skip", "park it" or "stop". Log every answer.

## Step 3 · Write PRD v0.1
Write it as a Claude Doc (use the docs skill), titled "PRD · <application name>", version and date at the top. Same 8 sections as /elicitation:
1. **Vision & scope**: why, for whom, what success looks like (the signals agreed in /scope-challenge). The scope map picture. The phases: MVP, Phase 2, Later, one line each. Out of scope, with the reason.
2. **User types**: who uses the app and for what (no permission details)
3. **Business objects**: functional data catalog. For each object (student, request, certificate, appointment, notification...): what it is, key information, statuses, who creates and updates it, and the business system it comes from when it is not created in the app. No database design.
4. **User stories**: As a [type], I want [action], so that [benefit]. ID, MoSCoW priority, phase, origin ("Workshop · scope map v<n>" or "Workshop · question Q<n>"). MVP features get full stories. Phase 2 and Later features get one line each, as epics, without acceptance criteria.
5. **Acceptance criteria** in Gherkin, grouped by business rule (Rule / Given / When / Then), for MVP stories only, built from the concrete examples given in the room
6. **Constraints**: only what cannot change (legal, GDPR, languages, accessibility, dates and peaks)
7. **Glossary**: one meaning per business term
8. **Decisions log**: every line of `scope-decisions.md`, then every answer of Step 2 (date · question · decision · who decided · owner if parked)

Stay functional: no permissions matrix, no technical design, no screen design.
Mark (Assumption) every rule the room did not state. Every system marked "to confirm" in the scope map appears in the Decisions log as parked, with an owner.

Then export the doc twice, next to each other in the project:
- `PRD-<application>-v0.1.docx` (Word) for the team
- `PRD-<application>-v0.1.md` (Markdown) for the agents, such as prd-griller
If Claude Docs is not available, write the PRD in Markdown and export it to Word with the docx skill.
End with: "Next: launch prd-griller in the background on PRD v0.1, and let us read it together."
