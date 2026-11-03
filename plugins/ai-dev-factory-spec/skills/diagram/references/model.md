# Diagram models

Plain JSON. Ids: short, lowercase, no spaces, unique in the file.

## Scope map

| Key | Content |
|---|---|
| `type` | `"scope"` |
| `title`, `subtitle` | Title, then version and date, for example `"v2 · 3 Nov 2026 · after challenge"` |
| `phases` | Ordered list. The first one is the MVP, drawn in red. Default `["MVP", "Later"]` |
| `app` | `{ "name", "description" }`: the application and its one-line promise |
| `users` | `[{ "id", "name", "label"? }]`: people who use the app (roles, not names) |
| `areas` | `[{ "id", "name", "features": [{ "name", "phase" }] }]`: capability areas and their features |
| `columns` | Optional, areas per row (default 3) |
| `systems` | `[{ "id", "name", "label", "dir", "tbc"? }]`: other systems. `label` = what flows. `dir`: `"in"` (data comes into the app), `"out"` (the app sends), `"both"` |
| `out_of_scope` | List of short items, shown in a band at the bottom |

```json
{
  "type": "scope",
  "title": "Student App · scope map",
  "subtitle": "v1 · draft to discuss",
  "phases": ["MVP", "Phase 2", "Later"],
  "app": { "name": "Student App", "description": "one mobile entry point for student life" },
  "users": [
    { "id": "stu", "name": "Student" },
    { "id": "staff", "name": "Student desk staff" }
  ],
  "areas": [
    { "id": "studies", "name": "My studies", "features": [
      { "name": "Timetable and room changes", "phase": "MVP" },
      { "name": "Exam registration", "phase": "Phase 2" } ] },
    { "id": "desk", "name": "Student desk", "features": [
      { "name": "Request a certificate", "phase": "MVP" } ] }
  ],
  "systems": [
    { "id": "acme", "name": "ACME", "label": "student record", "dir": "in" },
    { "id": "tick", "name": "Ticketing tool", "label": "requests", "dir": "both", "tbc": true }
  ],
  "out_of_scope": ["Admission (ACME portal)", "Payments"]
}
```

## Process map

| Key | Content |
|---|---|
| `type` | `"process"` |
| `title`, `subtitle` | Name of the process, version |
| `lanes` | `[{ "id", "name" }]`, top to bottom: the user first, then the app, then the back office and other systems |
| `steps` | `[{ "id", "lane", "text", "type"?, "next"?, "col"?, "tbc"? }]` |

- `type`: `"start"`, `"end"`, `"decision"` or `"task"` (default).
- `next`: list of step ids, or `{ "to", "label" }` for a decision exit (`"Yes"`, `"No"`).
- Columns are computed from the order of the flow. Set `"col"` on a step only to fix a crossing.
- A step that goes back to an earlier step (a loop, a correction) is drawn along the bottom of the lane.

```json
{
  "type": "process",
  "title": "Request a certificate",
  "subtitle": "Process map · v1",
  "lanes": [
    { "id": "s", "name": "Student" },
    { "id": "app", "name": "Student App" },
    { "id": "d", "name": "Student desk" }
  ],
  "steps": [
    { "id": "st", "lane": "s", "type": "start", "text": "Needs a certificate", "next": ["ask"] },
    { "id": "ask", "lane": "app", "text": "Pick the certificate type", "next": ["std"] },
    { "id": "std", "lane": "app", "type": "decision", "text": "Standard type?",
      "next": [ { "to": "get", "label": "Yes" }, { "to": "rev", "label": "No" } ] },
    { "id": "rev", "lane": "d", "text": "Review the request", "next": ["get"] },
    { "id": "get", "lane": "s", "type": "end", "text": "Downloads it" }
  ]
}
```
