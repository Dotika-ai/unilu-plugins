#!/usr/bin/env python3
"""Clean diagrams for the AI Dev Factory: a scope map or a process map, drawn from a JSON model.

Usage:
  python3 diagram.py model.json out/<name>

Writes, next to each other:
  <name>.excalidraw   full Excalidraw file (open on excalidraw.com, edit by hand)
  <name>.view.json    elements for the Excalidraw connector (create_view), to show it inline in Claude
  <name>.svg          vector image for slides and documents
  <name>.png          only if a converter is installed (rsvg-convert, cairosvg or playwright)

Model type "scope"  : users on the left, the application in the middle (capability areas and their
                      features, tagged by phase), the systems it talks to on the right, out of scope below.
Model type "process": one swimlane per actor, steps from left to right, decisions as diamonds.

Drawing rules (not negotiable): everything sits on a grid, arrows are straight lines, horizontal or
vertical, with right-angle bends only in the free gaps between columns. No diagonal, no curve,
no label on top of a box. Python standard library only.
"""
import json, os, shutil, subprocess, sys, random

INK, RED, GREY, MUTED, PAPER, CREAM, RULE, TINT = (
    "#1D1F30", "#E6332A", "#8A8780", "#606060", "#FFFFFF", "#FFFBF7", "#CBC8C5", "#FFF1EF")
FONT_W = 0.56          # average glyph width, as a share of the font size
_rng = random.Random(7)


# ------------------------------------------------------------------ primitives
class Canvas:
    def __init__(self):
        self.items = []    # dicts: kind = rect | diamond | text | line

    def rect(self, id_, x, y, w, h, text="", size=18, fill=PAPER, stroke=INK, color=INK,
             dash=False, width=2, bold=False, align="center", valign="middle", radius=True):
        self.items.append(dict(kind="rect", id=id_, x=x, y=y, w=w, h=h, text=text, size=size, fill=fill,
                               stroke=stroke, color=color, dash=dash, width=width, bold=bold,
                               align=align, valign=valign, radius=radius))

    def diamond(self, id_, x, y, w, h, text="", size=16, fill=PAPER, stroke=INK, color=INK):
        self.items.append(dict(kind="diamond", id=id_, x=x, y=y, w=w, h=h, text=text, size=size,
                               fill=fill, stroke=stroke, color=color, dash=False, width=2))

    def text(self, id_, x, y, w, s, size=16, color=INK, bold=False, align="left"):
        lines = wrap(s, w, size)
        self.items.append(dict(kind="text", id=id_, x=x, y=y, w=w, h=round(size * 1.25 * len(lines)),
                               text="\n".join(lines), size=size, color=color, bold=bold, align=align))

    def line(self, id_, pts, color=INK, dash=False, head_end=True, head_start=False, width=2,
             start=None, end=None):
        self.items.append(dict(kind="line", id=id_, pts=[(round(a), round(b)) for a, b in pts], color=color,
                               dash=dash, head_end=head_end, head_start=head_start, width=width,
                               start=start, end=end))

    def bounds(self):
        xs, ys = [], []
        for it in self.items:
            if it["kind"] == "line":
                xs += [p[0] for p in it["pts"]]; ys += [p[1] for p in it["pts"]]
            else:
                xs += [it["x"], it["x"] + it["w"]]; ys += [it["y"], it["y"] + it["h"]]
        return min(xs), min(ys), max(xs), max(ys)


def wrap(s, w, size):
    out = []
    per = max(6, int((w - 16) / (size * FONT_W)))
    for para in str(s).split("\n"):
        line = ""
        for word in para.split():
            if line and len(line) + 1 + len(word) > per:
                out.append(line); line = word
            else:
                line = (line + " " + word).strip()
        out.append(line)
    return out


def text_h(s, w, size):
    return round(size * 1.25 * len(wrap(s, w, size)))


# ------------------------------------------------------------------ scope map
PHASE_STYLE = [  # (stroke, fill, text colour, dashed)
    (RED, PAPER, INK, False),
    (GREY, PAPER, MUTED, True),
    (RULE, CREAM, GREY, True),
]


def scope(m, c):
    phases = m.get("phases") or ["MVP", "Later"]
    style = {p: PHASE_STYLE[min(i, 2)] for i, p in enumerate(phases)}
    UW, UH, SW, SH = 250, 76, 270, 76
    AW, FH, GAP = 300, 46, 14
    users, areas, systems = m.get("users", []), m.get("areas", []), m.get("systems", [])
    cols = max(1, min(int(m.get("columns") or 3), len(areas) or 1))
    X_APP = UW + 210
    Y0 = 120
    c.text("title", 0, 0, 1600, m.get("title", "Scope map"), 34, INK, True)
    c.text("subtitle", 0, 50, 1600, m.get("subtitle", "Scope map"), 18, MUTED)

    # areas grid inside the application frame
    heights = []
    for a in areas:
        h = 56 + sum(max(FH, text_h(f["name"], AW - 24, 16) + 18) + 10 for f in a.get("features", [])) + 6
        heights.append(h)
    rows = [list(range(i, min(i + cols, len(areas)))) for i in range(0, len(areas), cols)]
    fx, fy = X_APP, Y0
    inner_w = cols * AW + (cols - 1) * 28
    y = fy + 70
    for r in rows:
        rh = max(heights[i] for i in r)
        for k, i in enumerate(r):
            a = areas[i]
            ax = fx + 30 + k * (AW + 28)
            c.rect("area_" + a["id"], ax, y, AW, rh, "", fill=CREAM, stroke=RULE, width=1)
            c.text("area_t_" + a["id"], ax + 16, y + 14, AW - 32, a["name"].upper(), 15, MUTED, True)
            yy = y + 50
            for j, f in enumerate(a.get("features", [])):
                st, fi, tc, da = style.get(f.get("phase", phases[0]), PHASE_STYLE[1])
                fh = max(FH, text_h(f["name"], AW - 24, 16) + 18)
                c.rect(f"feat_{a['id']}_{j}", ax + 12, yy, AW - 24, fh, f["name"], 16, fi, st, tc, da,
                       2 if not da else 1.5, bold=f.get("phase", phases[0]) == phases[0])
                yy += fh + 10
        y += rh + 28
    frame_h = max(y - fy + 2, 2 * 90)
    app_name = m.get("app", {}).get("name", "Application")
    app_desc = m.get("app", {}).get("description", "")

    # users and systems, centred on the frame
    def stack(n, h, gap):
        tot = n * h + (n - 1) * gap
        return [fy + (frame_h - tot) / 2 + i * (h + gap) for i in range(n)]
    if users:
        frame_h = max(frame_h, len(users) * (UH + 34) + 40)
    if systems:
        frame_h = max(frame_h, len(systems) * (SH + 40) + 40)
    c.items.insert(2, dict(kind="rect", id="app", x=fx, y=fy, w=inner_w + 60, h=frame_h, text="", size=18,
                           fill="transparent", stroke=INK, color=INK, dash=True, width=2, bold=False,
                           align="center", valign="middle", radius=True))
    c.text("app_t", fx + 30, fy + 16, inner_w, app_name + (f"  ·  {app_desc}" if app_desc else ""), 20, INK, True)
    right = fx + inner_w + 60
    for u, uy in zip(users, stack(len(users), UH, 34)):
        c.rect("user_" + u["id"], 0, uy, UW, UH, u["name"], 18, INK, INK, PAPER, bold=True)
        cy = uy + UH / 2
        c.line("ua_" + u["id"], [(UW, cy), (fx, cy)], INK, start="user_" + u["id"], end="app")
        if u.get("label"):
            c.text("ual_" + u["id"], UW + 12, cy - 24, fx - UW - 24, u["label"], 14, MUTED, align="center")
    XS = right + 290
    for s, sy in zip(systems, stack(len(systems), SH, 40)):
        tbc = s.get("tbc")
        c.rect("sys_" + s["id"], XS, sy, SW, SH, s["name"] + ("\n(to confirm)" if tbc else ""), 17,
               "#ECEAE6", GREY, INK, tbc)
        cy = sy + SH / 2
        d = s.get("dir", "both")
        col = GREY if tbc else INK
        c.line("sa_" + s["id"], [(right, cy), (XS, cy)], col, tbc, head_end=d in ("out", "both"),
               head_start=d in ("in", "both"), start="app", end="sys_" + s["id"])
        if s.get("label"):
            lw = XS - right - 24
            c.text("sal_" + s["id"], right + 12, cy - 6 - text_h(s["label"], lw, 14), lw, s["label"], 14, MUTED,
                   align="center")
    bottom = fy + frame_h
    if m.get("out_of_scope"):
        items = m["out_of_scope"]
        w = XS + SW
        body = "   ·   ".join(items)
        h = text_h(body, w - 40, 16) + 60
        c.rect("oos", 0, bottom + 50, w, h, "", fill=PAPER, stroke=RULE, width=1)
        c.text("oos_t", 20, bottom + 64, 400, "OUT OF SCOPE", 15, RED, True)
        c.text("oos_b", 20, bottom + 90, w - 40, body, 16, INK)
        bottom += 50 + h
    # legend
    ly = bottom + 40
    x = 0
    for i, p in enumerate(phases):
        st, fi, tc, da = style[p]
        c.rect(f"lg_{i}", x, ly, 34, 22, "", fill=fi, stroke=st, dash=da, width=2 if not da else 1.5)
        c.text(f"lgt_{i}", x + 44, ly + 1, 200, p, 16, INK)
        x += 60 + len(p) * 10 + 40
    c.rect("lg_s", x, ly, 34, 22, "", fill="#ECEAE6", stroke=GREY)
    c.text("lgt_s", x + 44, ly + 1, 220, "Other system", 16, INK)
    x += 220
    c.rect("lg_t", x, ly, 34, 22, "", fill="#ECEAE6", stroke=GREY, dash=True)
    c.text("lgt_t", x + 44, ly + 1, 220, "To confirm", 16, INK)


# ------------------------------------------------------------------ process map
def process(m, c):
    lanes, steps = m["lanes"], m["steps"]
    LW, LH, CW, BW, BH = 210, 150, 300, 210, 76
    X0, Y0 = LW + 50, 110
    c.text("title", 0, 0, 1600, m.get("title", "Process"), 34, INK, True)
    c.text("subtitle", 0, 50, 1600, m.get("subtitle", "Process map"), 18, MUTED)
    lane_y = {l["id"]: Y0 + i * LH for i, l in enumerate(lanes)}
    byid = {s["id"]: s for s in steps}
    edges = []
    for s in steps:
        for n in s.get("next", []):
            n = {"to": n} if isinstance(n, str) else n
            edges.append((s["id"], n["to"], n.get("label", "")))
    # columns: longest forward path, back edges ignored (DFS)
    col, state = {}, {}
    back = set()

    def dfs(u):
        state[u] = 1
        for a, b, _ in edges:
            if a != u:
                continue
            if state.get(b) == 1:
                back.add((a, b)); continue
            if state.get(b) != 2:
                dfs(b)
        state[u] = 2
    for s in steps:
        if s["id"] not in state:
            dfs(s["id"])
    for s in steps:
        if "col" in s:
            col[s["id"]] = s["col"]
    changed = True
    for s in steps:
        col.setdefault(s["id"], 0)
    while changed:
        changed = False
        for a, b, _ in edges:
            if (a, b) in back or "col" in byid[b]:
                continue
            if col[b] < col[a] + 1:
                col[b] = col[a] + 1; changed = True
    ncol = max(col.values()) + 1
    width = X0 + ncol * CW
    for i, l in enumerate(lanes):
        y = lane_y[l["id"]]
        c.rect("lane_" + l["id"], 0, y, width, LH, "", fill=CREAM if i % 2 == 0 else PAPER, stroke=RULE, width=1,
               radius=False)
        c.text("lane_t_" + l["id"], 16, y + LH / 2 - text_h(l["name"], LW - 30, 17) / 2, LW - 30, l["name"], 17,
               INK, True)
    boxes = {}
    for s in steps:
        k = s.get("type", "task")
        cx = X0 + col[s["id"]] * CW + CW / 2
        cy = lane_y[s["lane"]] + LH / 2
        if k == "decision":
            w, h = 170, 104
            c.diamond(s["id"], cx - w / 2, cy - h / 2, w, h, s["text"], 15, TINT, RED)
        elif k in ("start", "end"):
            w, h = 150, 56
            c.rect(s["id"], cx - w / 2, cy - h / 2, w, h, s["text"], 16, INK, INK, PAPER, bold=True)
        else:
            w, h = BW, BH
            st, da = (GREY, True) if s.get("tbc") else (INK, False)
            c.rect(s["id"], cx - w / 2, cy - h / 2, w, h, s["text"], 16, PAPER, st, INK, da)
        boxes[s["id"]] = (cx - w / 2, cy - h / 2, w, h)
    occupied = {}
    for s in steps:
        occupied.setdefault((s["lane"], col[s["id"]]), s["id"])
    # arrows
    lane_of = {s["id"]: s["lane"] for s in steps}
    lane_idx = {l["id"]: i for i, l in enumerate(lanes)}
    used_gap = {}
    # a step with several exits: one leaves on the right, the others leave from the top or the bottom
    vexit, used_side = {}, {}
    for a, b, _ in edges:
        if (a, b) in back or col[b] <= col[a] or lane_of[a] == lane_of[b]:
            continue
        outs = [e for e in edges if e[0] == a and (e[0], e[1]) not in back]
        if len(outs) < 2:
            continue
        side = "bottom" if lane_idx[lane_of[b]] > lane_idx[lane_of[a]] else "top"
        lanes_between = range(min(lane_idx[lane_of[a]], lane_idx[lane_of[b]]) + 1,
                              max(lane_idx[lane_of[a]], lane_idx[lane_of[b]]))
        free_v = not any(occupied.get((lanes[i]["id"], col[a])) for i in lanes_between)
        free_h = not any(occupied.get((lane_of[b], j)) for j in range(col[a] + 1, col[b]))
        if free_v and free_h and side not in used_side.get(a, set()):
            vexit[(a, b)] = side
            used_side.setdefault(a, set()).add(side)
    # never send every exit up or down: keep the first one on the right when nothing else uses it
    for a in used_side:
        outs = [e for e in edges if e[0] == a and (e[0], e[1]) not in back]
        if all((a, e[1]) in vexit for e in outs):
            del vexit[(a, outs[0][1])]
    for k, (a, b, lab) in enumerate(edges):
        A, B = boxes[a], boxes[b]
        ca, cb = col[a], col[b]
        ay, by = A[1] + A[3] / 2, B[1] + B[3] / 2
        ax, bx = A[0] + A[2] / 2, B[0] + B[2] / 2
        if (a, b) in vexit:
            sy = A[1] + A[3] if vexit[(a, b)] == "bottom" else A[1]
            pts = [(ax, sy), (ax, by), (B[0], by)]
        elif cb > ca:
            between_b = any(occupied.get((lane_of[b], j)) for j in range(ca + 1, cb))
            between_a = any(occupied.get((lane_of[a], j)) for j in range(ca + 1, cb))
            if lane_of[a] == lane_of[b] and not between_a:
                pts = [(A[0] + A[2], ay), (B[0], by)]
            elif lane_of[a] == lane_of[b]:
                top = lane_y[lane_of[a]] + 14
                pts = [(ax, A[1]), (ax, top), (bx, top), (bx, B[1])]
            elif not between_b:
                g = X0 + (ca + 1) * CW - (CW - BW) / 2 + 0
                g = X0 + (ca + 1) * CW
                n = used_gap.get(ca, 0); used_gap[ca] = n + 1
                g -= 18 * n
                pts = [(A[0] + A[2], ay), (g, ay), (g, by), (B[0], by)]
            elif not between_a:
                g = X0 + cb * CW
                pts = [(A[0] + A[2], ay), (g, ay), (g, by), (B[0], by)]
            else:
                g1, g2 = X0 + (ca + 1) * CW, X0 + cb * CW
                lane_b = lane_y[lane_of[b]]
                yy = lane_b + 14 if lane_idx[lane_of[b]] > lane_idx[lane_of[a]] else lane_b + LH - 14
                pts = [(A[0] + A[2], ay), (g1, ay), (g1, yy), (g2, yy), (g2, by), (B[0], by)]
        else:  # back edge, along the bottom margin of the target lane
            yy = lane_y[lane_of[b]] + LH - 14
            ia, ib = lane_idx[lane_of[a]], lane_idx[lane_of[b]]
            if lane_of[a] == lane_of[b]:
                pts = [(ax, A[1] + A[3]), (ax, yy), (bx, yy), (bx, B[1] + B[3])]
            elif ia > ib and not any(occupied.get((lanes[i]["id"], cb)) for i in range(ib + 1, ia + 1)):
                ya = lane_y[lane_of[a]] + LH - 14
                pts = [(ax, A[1] + A[3]), (ax, ya), (bx, ya), (bx, B[1] + B[3])]
            else:
                g = X0 + (ca + 1) * CW
                pts = [(A[0] + A[2], ay), (g, ay), (g, yy), (bx, yy), (bx, B[1] + B[3])]
        c.line(f"e{k}_{a}_{b}", pts, INK, start=a, end=b)
        if lab:
            p, q = pts[0], pts[1]
            if abs(p[1] - q[1]) < 1:   # first segment horizontal: label above it
                c.text(f"el{k}", p[0] + 8, p[1] - 24, 80, lab, 14, RED, True)
            else:                      # first segment vertical: label beside it
                c.text(f"el{k}", p[0] + 8, p[1] + (6 if q[1] > p[1] else -24), 80, lab, 14, RED, True)


# ------------------------------------------------------------------ emitters
def _base(it, type_, **kw):
    e = dict(id=it["id"], type=type_, x=it.get("x", 0), y=it.get("y", 0), width=it.get("w", 0),
             height=it.get("h", 0), angle=0, strokeColor=INK, backgroundColor="transparent", fillStyle="solid",
             strokeWidth=2, strokeStyle="solid", roughness=0, opacity=100, groupIds=[], frameId=None,
             roundness=None, seed=_rng.randint(1, 2 ** 31), version=1, versionNonce=_rng.randint(1, 2 ** 31),
             isDeleted=False, boundElements=[], updated=1, link=None, locked=False)
    e.update(kw)
    return e


def _txt(id_, x, y, w, h, s, size, color, align="center", container=None, valign="middle"):
    return _base(dict(id=id_, x=x, y=y, w=w, h=h), "text", strokeColor=color, text=s, originalText=s,
                 fontSize=size, fontFamily=2, textAlign=align, verticalAlign=valign, containerId=container,
                 lineHeight=1.25, autoResize=True, boundElements=None)


def to_excalidraw(c):
    els, byid = [], {}
    for it in c.items:
        k = it["kind"]
        if k in ("rect", "diamond"):
            e = _base(it, "rectangle" if k == "rect" else "diamond", strokeColor=it["stroke"],
                      backgroundColor=it["fill"], strokeWidth=it["width"],
                      strokeStyle="dashed" if it["dash"] else "solid",
                      roundness={"type": 3} if it.get("radius", True) and k == "rect" else None)
            els.append(e); byid[it["id"]] = e
            if it["text"]:
                tw = it["w"] * (0.62 if k == "diamond" else 1)
                s = "\n".join(wrap(it["text"], tw, it["size"]))
                th = it["size"] * 1.25 * (s.count("\n") + 1)
                t = _txt(it["id"] + "_txt", it["x"] + (it["w"] - tw) / 2 + 8, it["y"] + (it["h"] - th) / 2, tw - 16,
                         th, s, it["size"], it["color"], container=it["id"])
                e["boundElements"].append({"type": "text", "id": t["id"]})
                els.append(t)
        elif k == "text":
            els.append(_txt(it["id"], it["x"], it["y"], it["w"], it["h"], it["text"], it["size"], it["color"],
                            it["align"], valign="top"))
        else:
            p0 = it["pts"][0]
            e = _base(dict(id=it["id"], x=p0[0], y=p0[1], w=max(abs(p[0] - p0[0]) for p in it["pts"]) or 1,
                           h=max(abs(p[1] - p0[1]) for p in it["pts"]) or 1), "arrow",
                      strokeColor=it["color"], strokeWidth=it["width"],
                      strokeStyle="dashed" if it["dash"] else "solid",
                      points=[[p[0] - p0[0], p[1] - p0[1]] for p in it["pts"]],
                      startArrowhead="arrow" if it["head_start"] else None,
                      endArrowhead="arrow" if it["head_end"] else None,
                      startBinding={"elementId": it["start"], "focus": 0, "gap": 2} if it.get("start") else None,
                      endBinding={"elementId": it["end"], "focus": 0, "gap": 2} if it.get("end") else None,
                      lastCommittedPoint=None, elbowed=False)
            els.append(e)
    for e in els:
        if e["type"] == "arrow":
            for bnd in (e.get("startBinding"), e.get("endBinding")):
                if bnd and bnd["elementId"] in byid:
                    byid[bnd["elementId"]]["boundElements"].append({"type": "arrow", "id": e["id"]})
    return {"type": "excalidraw", "version": 2, "source": "ai-dev-factory-spec/diagram", "elements": els,
            "appState": {"viewBackgroundColor": CREAM, "gridSize": None}, "files": {}}


def to_view(c):
    """Elements for the Excalidraw connector (create_view): one 4:3 camera on the whole drawing."""
    x0, y0, x1, y1 = c.bounds()
    w, h = x1 - x0 + 80, y1 - y0 + 80
    sizes = [(800, 600), (1200, 900), (1600, 1200), (2000, 1500), (2400, 1800), (3200, 2400)]
    cw, ch = next(((a, b) for a, b in sizes if a >= w and b >= h), sizes[-1])
    out = [{"type": "cameraUpdate", "width": cw, "height": ch, "x": round(x0 - (cw - w) / 2 - 40),
            "y": round(y0 - (ch - h) / 2 - 40)}]
    scale = max(1.0, cw / 1200)          # keep text readable on big cameras
    for it in c.items:
        k = it["kind"]
        if k in ("rect", "diamond"):
            e = {"type": "rectangle" if k == "rect" else "diamond", "id": it["id"], "x": round(it["x"]),
                 "y": round(it["y"]), "width": round(it["w"]), "height": round(it["h"]),
                 "strokeColor": it["stroke"], "backgroundColor": it["fill"], "fillStyle": "solid",
                 "strokeWidth": it["width"], "roughness": 0}
            if it["dash"]:
                e["strokeStyle"] = "dashed"
            if k == "rect" and it.get("radius", True):
                e["roundness"] = {"type": 3}
            if it["text"]:
                e["label"] = {"text": "\n".join(wrap(it["text"], it["w"] * (0.62 if k == "diamond" else 1),
                                                     it["size"])), "fontSize": it["size"],
                              "strokeColor": it["color"]}
            out.append(e)
        elif k == "text":
            out.append({"type": "text", "id": it["id"], "x": round(it["x"]), "y": round(it["y"]),
                        "text": it["text"], "fontSize": max(14, it["size"]), "strokeColor": it["color"]})
        else:
            p0 = it["pts"][0]
            e = {"type": "arrow", "id": it["id"], "x": p0[0], "y": p0[1],
                 "width": max(abs(p[0] - p0[0]) for p in it["pts"]) or 1,
                 "height": max(abs(p[1] - p0[1]) for p in it["pts"]) or 1,
                 "points": [[p[0] - p0[0], p[1] - p0[1]] for p in it["pts"]], "strokeColor": it["color"],
                 "strokeWidth": it["width"], "roughness": 0,
                 "endArrowhead": "arrow" if it["head_end"] else None,
                 "startArrowhead": "arrow" if it["head_start"] else None}
            if it["dash"]:
                e["strokeStyle"] = "dashed"
            out.append(e)
    _ = scale
    return out


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_svg(c):
    x0, y0, x1, y1 = c.bounds()
    pad = 40
    W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
         f'viewBox="{x0 - pad:.0f} {y0 - pad:.0f} {W:.0f} {H:.0f}" font-family="Manrope, Helvetica, Arial, sans-serif">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
         f'<rect x="{x0 - pad}" y="{y0 - pad}" width="{W}" height="{H}" fill="{CREAM}"/>']

    def tspan(x, y, s, size, color, anchor, bold):
        lines = s.split("\n")
        r = [f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
             f'{" font-weight=\"700\"" if bold else ""}>']
        for i, ln in enumerate(lines):
            r.append(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * 1.25:.1f}">{_esc(ln)}</tspan>')
        r.append("</text>")
        return "".join(r)

    for it in c.items:
        k = it["kind"]
        if k in ("rect", "diamond"):
            dash = ' stroke-dasharray="8 6"' if it["dash"] else ""
            fill = "none" if it["fill"] == "transparent" else it["fill"]
            if k == "rect":
                rx = 8 if it.get("radius", True) else 0
                o.append(f'<rect x="{it["x"]:.1f}" y="{it["y"]:.1f}" width="{it["w"]:.1f}" height="{it["h"]:.1f}" '
                         f'rx="{rx}" fill="{fill}" stroke="{it["stroke"]}" stroke-width="{it["width"]}"{dash}/>')
                tw = it["w"]
            else:
                x, y, w, h = it["x"], it["y"], it["w"], it["h"]
                o.append(f'<polygon points="{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}" '
                         f'fill="{fill}" stroke="{it["stroke"]}" stroke-width="{it["width"]}"{dash}/>')
                tw = it["w"] * 0.62
            if it["text"]:
                lines = wrap(it["text"], tw, it["size"])
                th = it["size"] * 1.25 * len(lines)
                ty = it["y"] + (it["h"] - th) / 2 + it["size"] * 0.95
                o.append(tspan(it["x"] + it["w"] / 2, ty, "\n".join(lines), it["size"], it["color"], "middle",
                               it.get("bold")))
        elif k == "text":
            anchor = {"left": "start", "center": "middle"}.get(it["align"], "start")
            x = it["x"] + (it["w"] / 2 if anchor == "middle" else 0)
            o.append(tspan(x, it["y"] + it["size"] * 0.95, it["text"], it["size"], it["color"], anchor, it["bold"]))
        else:
            pts = " ".join(f"{a},{b}" for a, b in it["pts"])
            dash = ' stroke-dasharray="8 6"' if it["dash"] else ""
            ms = ' marker-start="url(#ah)"' if it["head_start"] else ""
            me = ' marker-end="url(#ah)"' if it["head_end"] else ""
            o.append(f'<polyline points="{pts}" fill="none" stroke="{it["color"]}" stroke-width="{it["width"]}"'
                     f'{dash}{ms}{me} stroke-linejoin="miter"/>')
    o.append("</svg>")
    return "\n".join(o)


def to_png(svg_path, png_path):
    if shutil.which("rsvg-convert"):
        return subprocess.call(["rsvg-convert", "-z", "2", "-o", png_path, svg_path]) == 0
    try:
        import cairosvg  # noqa
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2)
        return True
    except Exception:
        pass
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(device_scale_factor=2)
            pg.goto("file://" + os.path.abspath(svg_path))
            pg.locator("svg").screenshot(path=png_path)
            b.close()
        return True
    except Exception:
        return False


def check(c):
    """Return problems: overlapping boxes, arrows crossing boxes, non orthogonal segments."""
    probs = []
    boxes = [it for it in c.items if it["kind"] in ("rect", "diamond") and not it["id"].startswith(("area_", "lane_", "app", "oos", "lg"))]
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]:
                probs.append(f"overlap: {a['id']} / {b['id']}")
    for ln in [it for it in c.items if it["kind"] == "line"]:
        for p, q in zip(ln["pts"], ln["pts"][1:]):
            if p[0] != q[0] and p[1] != q[1]:
                probs.append(f"diagonal segment in {ln['id']}")
            for b in boxes:
                if b["id"] in (ln.get("start"), ln.get("end")):
                    continue
                lx0, lx1, ly0, ly1 = min(p[0], q[0]), max(p[0], q[0]), min(p[1], q[1]), max(p[1], q[1])
                if lx0 < b["x"] + b["w"] - 1 and b["x"] + 1 < lx1 + (1 if lx0 == lx1 else 0) and \
                        ly0 < b["y"] + b["h"] - 1 and b["y"] + 1 < ly1 + (1 if ly0 == ly1 else 0):
                    probs.append(f"{ln['id']} crosses {b['id']}")
    return probs


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        m = json.load(f)
    c = Canvas()
    {"scope": scope, "process": process}[m.get("type", "scope")](m, c)
    out = sys.argv[2]
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    with open(out + ".excalidraw", "w", encoding="utf-8") as f:
        json.dump(to_excalidraw(c), f, ensure_ascii=False, indent=1)
    with open(out + ".view.json", "w", encoding="utf-8") as f:
        json.dump(to_view(c), f, ensure_ascii=False, separators=(",", ":"))
    with open(out + ".svg", "w", encoding="utf-8") as f:
        f.write(to_svg(c))
    png = to_png(out + ".svg", out + ".png")
    probs = check(c)
    print("ok", out + ".excalidraw", out + ".view.json", out + ".svg", out + ".png" if png else "(no png converter)")
    print("checks:", "clean" if not probs else "\n- " + "\n- ".join(probs))


if __name__ == "__main__":
    main()
