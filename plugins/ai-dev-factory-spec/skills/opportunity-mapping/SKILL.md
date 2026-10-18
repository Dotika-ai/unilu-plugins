---
name: opportunity-mapping
description: This skill should be used after /elicitation, when the team asks to "extend the scope", "propose new features", "challenge the scope", "find opportunities" or calls /opportunity-mapping. It proposes genuinely new ideas on top of PRD v0.1 (better journeys, good practices from other products, AI-enabled features), one at a time, and the team decides.
---

# Opportunity mapping · extend the scope, on purpose

Goal: go beyond the existing. Suggest what the product could do better, then let the team decide.

## Step 1 · Map NEW opportunities
Read the PRD doc (v0.1) first: everything in it is already known. Your job is to bring what is NOT in it.
Stay within the scope set in the project instructions and in Vision & scope: only propose ideas for the part of the product being built.
Generate ideas in 4 families:
1. Rethink the journey: steps that could disappear, be merged, be automated or done in self-service
2. Good practices from other products and other universities: clarity, mobile, accessibility, languages, real-time status, reminders
3. AI for each user type: what an assistant, an automatic check or a smart triage would change for them
4. Data that already exists and could be reused: pre-filled forms, documents asked only once, information shared between steps
For each idea: title · who benefits · problem solved · value (H/M/L) · business complexity (H/M/L).

Novelty check, before presenting anything:
- Read every request listed in the sources, including those the client tagged as new or as improvement requests. They are already known.
- Drop every idea that is already in PRD v0.1, already listed as a request in the sources, or only rephrases one of them.
- Keep at least 8 ideas. If fewer survive, generate more.
- For each idea kept, write one line: "New because…".

## Step 2 · Present one at a time
Start with the highest value and lowest complexity. Show O3/10, pitch the idea in 3 lines including "New because…", then ask: Accept, Reject or Park?
Accept "skip" or "stop" at any time. On stop, or when the list is done, go to Step 3.
Stay functional. No technical design.

## Step 3 · Update the PRD doc
Update the same Claude Doc and keep the structure set by /elicitation.
- Accepted: add user stories and Gherkin acceptance criteria, marked (Workshop idea), with "Workshop" as origin. Add any new business object or term.
Use no other tags, codes or abbreviations.
- Rejected: add to the out-of-scope list in Vision & scope, with the reason.
- Parked: log it in the Decisions log as parked, with an owner.
Log every decision in the Decisions log. Set the version to v0.2, then export the doc to Word (PRD-<module>-v0.2.docx) and to Markdown (PRD-<module>-v0.2.md).
