---
name: diagram
description: This skill should be used whenever a scope map or a process map must be drawn or redrawn for the AI Dev Factory, by /scope-map, /scope-challenge or /prd-draft, or when the team asks to "draw the scope", "draw the process", "redraw the diagram", "make it clean", "show it in Excalidraw". It turns a small JSON model into a clean Excalidraw diagram (grid layout, straight arrows) plus SVG and PNG.
---

# Diagram · clean scope maps and process maps

Never draw the diagram by hand, element by element. Write or update the JSON model, then run the script: it places everything on a grid and draws only straight arrows, horizontal or vertical. A diagram drawn freehand ends up with diagonal arrows, overlaps and labels on top of boxes; this skill exists to avoid that.

## Two kinds of diagram
- **scope**: who uses the application (left), what it does, grouped by capability area and tagged by phase (centre), which other systems it talks to (right), what is out of scope (bottom). Use it to agree on the scope.
- **process**: one swimlane per actor or system, steps from left to right, decisions as diamonds with Yes/No exits. Use it for one key journey.

The model format and a full example of each are in `references/model.md`. Read it before writing a model.

## Steps
1. Write the model to `<name>.json` in the working folder (for example `scope-map.json`, `process-request-certificate.json`). Keep the previous version: `scope-map-v1.json`, `scope-map-v2.json`...
2. Find the script once: `${CLAUDE_PLUGIN_ROOT}/skills/diagram/scripts/diagram.py`. If that variable is empty, run `find / -name diagram.py -path "*diagram/scripts*" 2>/dev/null | head -1`.
3. Run it: `python3 <script> <name>.json <output folder>/<name>`. It writes `<name>.excalidraw`, `<name>.view.json`, `<name>.svg` and, when a converter exists, `<name>.png`. Standard library only, nothing to install.
4. Read the last line it prints. If it is not `checks: clean` (overlap, arrow crossing a box), fix the model: shorten a label, move a step to another column with `"col"`, split an area. Run again.
5. Show it:
   - If the Excalidraw connector is on, call its `create_view` tool with the exact content of `<name>.view.json` as `elements`. Do not edit the elements and do not add any.
   - Otherwise show the PNG (or the SVG).
   - Always give the `.excalidraw` file: the team opens it on excalidraw.com to move a box by hand.
6. Look at the image before saying it is done. Readable in 10 seconds, or it is not finished.

## Readability rules
- Scope map: 3 to 6 users, 3 to 6 capability areas, 2 to 6 features per area, 3 to 8 other systems. More than that: group, or move details to the PRD.
- Process map: 3 to 6 lanes, 12 steps at most. One process per diagram.
- Labels: 2 to 6 words, the business words of the university. No technical names unless the business uses them.
- Anything not confirmed by the room: `"tbc": true` (drawn dashed, "to confirm").
- The JSON model is the source of truth. A change asked in the room goes into the model, then the diagram is redrawn. Never patch the picture.
