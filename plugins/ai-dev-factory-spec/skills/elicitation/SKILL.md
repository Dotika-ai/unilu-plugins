---
name: elicitation
description: This skill should be used when the team asks to "run the elicitation", "validate our understanding", "restate what exists", "go through the questions" or calls /elicitation. It restates the existing documentation (processes, user stories, improvement requests), validates it with functional questions asked one at a time, and produces PRD v0.1.
---

# Elicitation · validate a shared understanding

Goal: make sure the team shares the same understanding of what exists today (AS-IS) and what is asked (TO-BE), BEFORE adding anything new.
Scope: what is in the sources, within the scope set in the project instructions. Do not propose new features here: that is the job of /opportunity-mapping.
If the project instructions put part of the product out of scope, ignore the requests that only concern that part: do not list them, do not ask about them, do not turn them into user stories.

## Step 1 · Restate, so that anyone in the room understands
Read the project instructions: they list every source document and when to use it. Then read the sources needed.
This restatement is read on a big screen by business people who did not read the documents. It must be easy to scan: short lines, clear headings, white space. Detail is welcome, walls of text are not.

Deliver it in two messages, so each one fits on the screen.

**Message 1 · The picture**

**In short** · 3 bullets: what the module is and who uses it · why it is being rebuilt · what today's session must produce.

**1. The problem and the objectives** · Two short lists: "What goes wrong today" and "What success looks like". 3 to 6 bullets each.

**2. Who uses it** · A table with 3 columns: user type · what they do · when.

**3. How it works today** · A numbered list, one step per line: who does what, then what happens. Put the exceptions (missing documents, refusal, appeal, waiting list...) as indented bullets under the step where they happen.

End message 1 with: "Is this right so far? Say ok and I show what is asked." Then wait.

**Message 2 · What is asked**

**4. What is asked** · Every request found in the sources, none left out, none merged. Start with one line giving the count per theme and per client tag. Then one heading per theme, with its count, for example "Document management · 9 requests". Under it, one bullet per request: **short title in bold** · for whom · the client's own tag and priority if the source gives one (for example AS-IS, IMPROVEMENT REQUEST, NEW, High). One line per request: keep the details for the questions. If the sources already contain user stories, restate each one this way and keep its tag: they are the starting point, not something to rewrite from scratch.

**5. What I am not sure about** · 5 to 10 bullets, one gap or assumption each. These become the questions of Step 2.

End message 2 with: "Is this picture right? If so, let's go through my questions, one at a time." Then wait.

Writing rules, for both messages:
- Bullets, not paragraphs. One idea per bullet, 20 words maximum. Start each bullet with its key words in bold.
- Full words, no telegraphic shorthand.
- Explain every acronym the first time it appears, for example "SEVE (Service des Études et de la Vie Étudiante, the studies and student life office)".
- Use the university's words, not technical ones. No data model, no system names unless the business uses them.
- Give one concrete example when a rule is abstract, for example "a non-EU candidate applying to a Bachelor".
- Sources: end each section with one line "Sources: <file names>". Inside the text, mark only what no source says, with (Assumption). Do not label every line. Copy the client's own tags exactly as they appear in the sources. No other tags, codes or abbreviations.

## Step 2 · Ask, one question at a time
Prepare the questions internally and order them by impact on the scope. Then:
- Ask ONE question per message. Never more.
- Format: Q3/12 · the question · why it matters (1 line) · best guess, if any.
- Ask functional and business-process questions only: who, what, when, which rule, which exception, which volume, which decision. Never technical.
- Cover the existing requests first: the ones that are vague, that conflict with each other or with how it works today, that have no clear rule or example, and the ones with no priority. Ask the room to confirm or change the client's tag and priority when it matters for the scope.
- Prefer closed or multiple-choice questions so the room can answer fast.
- After each answer: acknowledge in one line, update the understanding, ask the next question.
- If an answer contradicts a source, say so and ask which one wins.
- Accept "skip", "park it" or "stop" at any time.

## Step 3 · Write PRD v0.1
When the questions are done (or the team says stop), write PRD v0.1 as a Claude Doc (use the docs skill), titled "PRD · <module name>", with the version and the date at the top. Use this structure:
1. Vision & scope: why, for whom, what success looks like, what is in and out.
2. User types: who uses the module and for what (no permission details)
3. Business objects: a functional data catalog. For each object (candidate, application file, programme, document, decision, payment...): what it is, its key information, its statuses, who creates and updates it. No database design.
4. User stories: As a [type], I want [action], so that [benefit]; each with an ID, a MoSCoW priority and its origin (the client's tag and source file, for example "IMPROVEMENT REQUEST · <source file>"). Include every request validated in Step 2.
5. Acceptance criteria in Gherkin, grouped by business rule (Rule / Given / When / Then)
6. Constraints: only what cannot change (legal, languages, deadlines and peaks). Keep it short.
7. Glossary: one meaning per business term
8. Decisions log: a table (date · question · decision · who decided · owner if parked), parked questions included

Stay functional: no permissions matrix, no process maps, no technical design.
Build the Gherkin scenarios from concrete examples given in the answers.
Add every business term that came up to the Glossary.
Log every answer in the Decisions log.
Then export the doc twice, next to each other in the project:
- PRD-<module>-v0.1.docx (Word) for the team
- PRD-<module>-v0.1.md (Markdown) for the agents, such as prd-griller
If Claude Docs is not available, write the PRD in Markdown and export it to Word with the docx skill.
