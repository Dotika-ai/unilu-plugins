---
name: scope-map
description: This skill should be used at the start of a greenfield project (a new application, no existing documentation), when the team asks to "map the scope", "draw the application", "agree on what the app does", "start from a blank page" or calls /scope-map. It collects the room's ideas, asks a few questions one at a time, proposes a first scope map (users, capability areas, features by phase, other systems, out of scope) and draws it cleanly, then redraws it live as the room corrects it.
---

# Scope map · agree on what we build, on one picture

Goal: in about 30 minutes, the room agrees on ONE picture of the application: who uses it, what it does, in which phase, what it talks to, and what it does not do.
This is the greenfield counterpart of /elicitation: there is nothing to restate, so we build the picture with the room. No PRD yet: /prd-draft writes it from this picture.
Stay functional: users, needs, features, business systems. No architecture, no technology.

## Step 1 · Collect, in one go
Ask one open question and wait:
"Tell me everything you have in mind about this application, in any order: who will use it, what goes wrong today without it, what it must do, what already exists, what it must not become. Dictate freely; I will structure it."
Then restate in one short message, easy to scan on a big screen:
- **In short** · 3 bullets: what the app is, for whom, why now
- **Users** · one line each
- **Needs** · grouped by theme, one line each, in the room's words
- **Already exists elsewhere** · tools, websites, apps, desks the users rely on today
- **Not sure** · 3 to 6 gaps
End with: "Is this the right raw material? Say ok and I ask a few questions before drawing."

## Step 2 · Ask, one question at a time, 5 questions at most
Only what blocks the drawing. Order by impact on the scope. Format: Q2/5 · the question · why it matters (1 line) · best guess.
Typical gaps: the primary user of the first version; the one need that justifies the app on day one; which data already exists and where (the business name of the system, for example ACME); what the app replaces or must not duplicate; a hard date (start of the academic year, a peak).
Prefer closed or multiple-choice questions. Accept "skip" or "stop" at any time. Log every answer as a decision.

## Step 3 · Propose a first scope map
Build the model (format in the diagram skill, `references/model.md`):
- `phases`: `["MVP", "Phase 2", "Later"]` unless the room set others
- 3 to 6 users, 3 to 6 capability areas, 2 to 6 features per area, in the university's words
- every feature gets a phase. MVP = the smallest set that is worth releasing for the primary user. When in doubt, Phase 2
- every other system gets a label (what flows) and a direction; mark `"tbc": true` what the room did not confirm
- `out_of_scope`: what the room said the app must not do, and the neighbours it must not duplicate
- subtitle: `v1 · <date> · proposal`
Draw it with the **diagram** skill (`scope-map-v1.json`). Under the picture, list in 3 to 6 bullets the choices YOU made that the room did not state, marked (Assumption). Ask: "What do we change?"

## Step 4 · Correct it live
The room reacts by voice, in any order. For each piece of feedback:
1. Say in one line what changes in the model (add, remove, rename, move to another phase, confirm a system)
2. If it contradicts an earlier decision, say so and ask which one wins
3. Update the model, keep the version number, redraw after every 2 or 3 changes, or when asked ("redraw")
4. Log the decision: date · what was asked · decision · who decided

## Step 5 · Freeze the scope map
When the room says "scope ok" (or "freeze"):
- set the subtitle to `v<n> · <date> · agreed in the workshop`, save `scope-map-v<n>.json`, redraw, give the `.excalidraw` and the PNG
- write `scope-decisions.md`: a table (date · question · decision · who decided · owner if parked). /scope-challenge and /prd-draft continue it, and /prd-draft moves it into the PRD Decisions log
- end with: "Next: /scope-challenge to stress-test the MVP, then /prd-draft."

Writing rules: bullets, not paragraphs, 20 words maximum each, key words in bold. Explain every acronym the first time. The university's words, not technical ones.
