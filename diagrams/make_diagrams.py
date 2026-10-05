"""Generate the course diagrams (SVG) in one consistent style.

    python diagrams/make_diagrams.py        writes diagrams/*.svg

Each diagram is described with a few primitives (boxes, commits, arrows, labels), so they stay editable and match.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Cascadia Code, Consolas, Menlo, monospace"
INK, MUTED, LINE, BG = "#1f2937", "#5b6472", "#c9d1dc", "#ffffff"
BLUE, GREEN, ORANGE, PURPLE, RED, TEAL = "#2563eb", "#16a34a", "#ea7a0c", "#7c3aed", "#dc2626", "#0d9488"


class Svg:
    def __init__(self, w: int, h: int, title: str):
        self.w, self.h, self.parts = w, h, []
        self.parts.append(f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>')
        self.text(24, 38, title, size=20, weight=700)

    def text(self, x, y, s, size=14, color=INK, weight=400, anchor="start", mono=False):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        fam = MONO if mono else FONT
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
                          f'fill="{color}" text-anchor="{anchor}" xml:space="preserve">{s}</text>')

    def box(self, x, y, w, h, title, sub="", color=BLUE, fill=None):
        fill = fill or color + "14"
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{color}" stroke-width="2"/>')
        self.text(x + w / 2, y + (h / 2 + 5 if not sub else h / 2 - 6), title, size=15, weight=700, anchor="middle", color=color)
        if sub:
            self.text(x + w / 2, y + h / 2 + 15, sub, size=12, color=MUTED, anchor="middle")

    def commit(self, x, y, label, color=BLUE, hollow=False, below=""):
        fill = BG if hollow else color
        dash = ' stroke-dasharray="4 3"' if hollow else ""
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{fill}" stroke="{color}" stroke-width="2.5"{dash}/>')
        self.text(x, y + 5, label, size=13, weight=700, anchor="middle", color=color if hollow else "#ffffff", mono=True)
        if below:
            self.text(x, y + 38, below, size=11, anchor="middle", color=MUTED)

    def line(self, x1, y1, x2, y2, color=LINE, width=3, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash}/>')

    def arrow(self, x1, y1, x2, y2, label="", color=MUTED, above=True, dashed=False):
        mid = f"a{len(self.parts)}"
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.parts.append(f'<defs><marker id="{mid}" markerWidth="11" markerHeight="11" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
                          f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker></defs>')
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.2"{dash} '
                          f'marker-end="url(#{mid})"/>')
        if label:
            self.text((x1 + x2) / 2, (y1 + y2) / 2 + (-9 if above else 20), label, size=13, anchor="middle",
                      color=color, mono=True)

    def tag(self, x, y, label, color=GREEN):
        w = 9 * len(label) + 16
        self.parts.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="24" rx="12" fill="{color}"/>')
        self.text(x, y + 4, label, size=12, weight=700, anchor="middle", color="#ffffff", mono=True)

    def save(self, name: str):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
               f'height="{self.h}" role="img" aria-label="{name}">' + "".join(self.parts) + "</svg>\n")
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote diagrams/{name}.svg")


def architecture():
    d = Svg(1000, 330, "Where your changes live")
    cols = [("Working directory", "your files", ORANGE), ("Staging area", "the next commit", PURPLE),
            ("Local repository", ".git: commits", BLUE), ("Remote repository", "GitHub: origin", GREEN)]
    for i, (t, s, c) in enumerate(cols):
        d.box(20 + i * 250, 110, 180, 90, t, s, c)
    d.arrow(204, 140, 266, 140, "add")
    d.arrow(454, 140, 516, 140, "commit")
    d.arrow(704, 140, 766, 140, "push")
    d.arrow(766, 175, 704, 175, "fetch", above=False)
    d.arrow(266, 175, 204, 175, "restore", above=False)
    d.text(500, 255, "git status shows the first two columns · git log shows the third · git fetch updates origin/*",
           size=13, color=MUTED, anchor="middle")
    d.text(500, 285, "git pull = fetch + merge (or rebase) · git switch moves the working directory to another commit",
           size=13, color=MUTED, anchor="middle")
    d.save("01-git-architecture")


def remotes():
    d = Svg(1000, 380, "Local branches, remote-tracking branches and the server")
    d.box(40, 80, 400, 250, "", color=BLUE, fill="#2563eb08")
    d.text(60, 110, "your clone", size=15, weight=700, color=BLUE)
    d.box(560, 80, 400, 250, "", color=GREEN, fill="#16a34a08")
    d.text(580, 110, "server (GitHub)", size=15, weight=700, color=GREEN)
    for i, c in enumerate("ABC"):
        d.commit(100 + i * 80, 190, c)
        d.commit(620 + i * 80, 190, c, GREEN)
    d.line(117, 190, 163, 190); d.line(197, 190, 243, 190)
    d.line(637, 190, 683, 190); d.line(717, 190, 763, 190)
    d.commit(860, 190, "D", GREEN)
    d.line(797, 190, 843, 190)
    d.tag(260, 150, "main"); d.tag(180, 245, "origin/main", TEAL)
    d.tag(860, 150, "main")
    d.text(240, 296, "origin/main = main on the server at your last fetch", size=12, color=MUTED, anchor="middle")
    d.text(240, 316, "git fetch brings D and moves origin/main", size=12, color=TEAL, anchor="middle")
    d.arrow(560, 222, 440, 222, "git fetch", color=TEAL, above=False)
    d.arrow(440, 160, 560, 160, "git push", color=BLUE)
    d.save("02-remotes")


def branches_merge():
    d = Svg(1000, 420, "Branches and the two kinds of merge")
    d.text(30, 80, "fast-forward: main had not moved", size=15, weight=700, color=BLUE)
    for i, c in enumerate(["A", "B"]):
        d.commit(70 + i * 80, 140, c)
    d.line(87, 140, 133, 140)
    d.commit(230, 140, "C", ORANGE); d.line(167, 140, 213, 140, ORANGE)
    d.tag(230, 100, "feature", ORANGE); d.tag(150, 100, "main")
    d.arrow(270, 140, 330, 140, "merge")
    for i, c in enumerate(["A", "B", "C"]):
        d.commit(370 + i * 80, 140, c)
    d.line(387, 140, 433, 140); d.line(467, 140, 513, 140)
    d.tag(530, 100, "main, feature")
    d.text(450, 195, "the label just moves forward: no merge commit", size=12, color=MUTED, anchor="middle")

    d.text(30, 235, "three-way: both branches moved", size=15, weight=700, color=PURPLE)
    d.commit(70, 330, "A"); d.commit(150, 330, "B", below="merge base")
    d.line(87, 330, 133, 330)
    d.commit(240, 290, "C", ORANGE); d.line(165, 320, 224, 297, ORANGE)
    d.commit(240, 370, "D"); d.line(165, 340, 224, 365)
    d.tag(300, 290, "feature", ORANGE)
    d.arrow(285, 330, 345, 330, "merge")
    d.commit(390, 330, "A"); d.commit(470, 330, "B")
    d.line(407, 330, 453, 330)
    d.commit(560, 290, "C", ORANGE); d.line(485, 320, 544, 297, ORANGE)
    d.commit(560, 370, "D"); d.line(485, 340, 544, 365)
    d.commit(660, 330, "M", PURPLE); d.line(576, 297, 644, 323, ORANGE); d.line(576, 365, 644, 337)
    d.tag(660, 290, "main", BLUE)
    d.text(800, 315, "M has two parents.", size=13, color=INK)
    d.text(800, 335, "Same lines changed on both", size=13, color=INK)
    d.text(800, 355, "sides → CONFLICT (lesson 26)", size=13, color=RED)
    d.save("03-branches-and-merge")


def rebase():
    d = Svg(1000, 330, "Rebase: replay your commits on a new base")
    d.text(30, 80, "before", size=15, weight=700, color=MUTED)
    d.commit(70, 180, "A"); d.commit(150, 180, "B"); d.line(87, 180, 133, 180)
    d.commit(240, 230, "D"); d.line(165, 190, 224, 223); d.tag(240, 270, "main", BLUE)
    d.commit(240, 130, "C1", ORANGE); d.commit(320, 130, "C2", ORANGE)
    d.line(165, 170, 224, 137, ORANGE); d.line(257, 130, 303, 130, ORANGE)
    d.tag(320, 95, "feature", ORANGE)
    d.arrow(380, 180, 450, 180, "git rebase main")
    d.text(500, 80, "after", size=15, weight=700, color=MUTED)
    for i, c in enumerate(["A", "B", "D"]):
        d.commit(520 + i * 80, 180, c)
    d.line(537, 180, 583, 180); d.line(617, 180, 663, 180)
    d.commit(760, 180, "C1'", ORANGE); d.commit(840, 180, "C2'", ORANGE)
    d.line(697, 180, 743, 180, ORANGE); d.line(777, 180, 823, 180, ORANGE)
    d.tag(680, 225, "main", BLUE); d.tag(840, 140, "feature", ORANGE)
    d.commit(760, 105, "C1", ORANGE, hollow=True); d.commit(840, 105, "C2", ORANGE, hollow=True)
    d.text(900, 85, "old commits: reflog only", size=11, color=MUTED, anchor="end")
    d.text(500, 300, "C1' and C2' are new commits (new IDs). Never rebase commits others have built on.",
           size=13, color=RED, anchor="middle")
    d.save("04-rebase")


def reset():
    d = Svg(1000, 380, "git reset: what each mode resets")
    heads = ["", "HEAD / branch", "Staging area (index)", "Working directory"]
    rows = [("--soft", ["moves", "kept", "kept"], GREEN),
            ("--mixed (default)", ["moves", "reset", "kept"], ORANGE),
            ("--hard", ["moves", "reset", "reset (uncommitted work lost!)"], RED)]
    for i, h in enumerate(heads):
        d.text(60 + i * 230, 100, h, size=14, weight=700, color=MUTED)
    for r, (mode, cells, color) in enumerate(rows):
        y = 140 + r * 70
        d.box(40, y - 25, 190, 50, mode, color=color)
        for c, cell in enumerate(cells):
            col = RED if "lost" in cell else (INK if cell == "moves" else (MUTED if cell == "kept" else color))
            d.text(290 + c * 230, y + 5, cell, size=14, color=col, weight=700 if cell != "kept" else 400)
    d.text(500, 350, "Commits left behind by reset are still recoverable with git reflog / ORIG_HEAD (lessons 33, 81).",
           size=13, color=MUTED, anchor="middle")
    d.save("05-reset-three-trees")


def reflog():
    d = Svg(1000, 330, "The reflog: where HEAD has been")
    d.box(40, 70, 560, 220, "", color=PURPLE, fill="#7c3aed08")
    lines = [("HEAD@{0}", "reset: moving to HEAD~3", RED), ("HEAD@{1}", "commit: Price mocha", INK),
             ("HEAD@{2}", "commit: Add mocha", INK), ("HEAD@{3}", "commit: Price green tea", INK),
             ("HEAD@{4}", "checkout: moving from main to v1.0.0", INK)]
    for i, (ref, msg, color) in enumerate(lines):
        d.text(70, 115 + i * 36, ref, size=15, color=PURPLE, mono=True, weight=700)
        d.text(190, 115 + i * 36, msg, size=15, color=color, mono=True)
    d.arrow(620, 151, 700, 151, "", color=GREEN)
    d.text(710, 145, "git reset --hard HEAD@{1}", size=14, color=GREEN, mono=True)
    d.text(710, 168, "or git branch rescue HEAD@{1}", size=14, color=GREEN, mono=True)
    d.text(710, 215, "local to your clone, never pushed;", size=13, color=MUTED)
    d.text(710, 235, "entries expire after 30–90 days", size=13, color=MUTED)
    d.save("06-reflog")


def pull_request():
    d = Svg(1000, 300, "A pull request")
    steps = [("Feature branch", "pushed", ORANGE), ("Pull request", "branch vs main", BLUE),
             ("Review", "comments, approval", PURPLE), ("Checks", "CI must be green", TEAL), ("Merge", "into main", GREEN)]
    for i, (t, s, c) in enumerate(steps):
        d.box(20 + i * 196, 110, 170, 80, t, s, c)
        if i:
            d.arrow(i * 196 - 6, 150, i * 196 + 18, 150)
    d.text(500, 250, "Protected main: no direct pushes, required review and checks (lesson 59)",
           size=13, color=MUTED, anchor="middle")
    d.save("07-pull-request")


def cicd():
    d = Svg(1000, 360, "From a developer's commit to Kubernetes")
    row1 = [("Developer", "", INK), ("Feature branch", "commit, push", ORANGE), ("Pull request", "review", BLUE),
            ("Checks", "GitHub Actions", TEAL), ("Merge", "main", GREEN)]
    row2 = [("Tag v1.0.0", "release", GREEN), ("Actions", "release workflow", TEAL), ("Docker image", "build", BLUE),
            ("GHCR", "registry", PURPLE), ("Helm → Kubernetes", "deploy", ORANGE)]
    for i, (t, s, c) in enumerate(row1):
        d.box(20 + i * 196, 80, 170, 70, t, s, c)
        if i:
            d.arrow(i * 196 - 6, 115, i * 196 + 18, 115)
    d.arrow(895, 155, 895, 205)
    for i, (t, s, c) in enumerate(reversed(row2)):
        d.box(20 + i * 196, 210, 170, 70, t, s, c)
        if i:
            d.arrow(i * 196 + 18, 245, i * 196 - 6, 245)
    d.text(500, 325, "Module 21 and the capstone run this whole chain; rollback = redeploy the previous tag",
           size=13, color=MUTED, anchor="middle")
    d.save("08-devops-cicd")


if __name__ == "__main__":
    for f in (architecture, remotes, branches_merge, rebase, reset, reflog, pull_request, cicd):
        f()
