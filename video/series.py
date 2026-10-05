"""The video series, generated from the lessons: one video per module, plus the DevOps workflow, the troubleshooting
labs and the capstone.

Every lesson becomes the same five scenes, played as a conversation between a senior DevOps engineer and a junior
colleague (two voices):

  concept    the junior asks; the senior explains, with the lesson's diagram on screen
  demo       the lab and the demonstration commands, with their real outputs (recorded when the tests ran)
  break      the junior makes the lesson's mistake on purpose (error tone); the senior reads the symptoms
  fix        the fix, with its real output (success chime)
  recap      the three points to remember

Nothing on screen is typed by hand: commands and outputs are the lesson's tested blocks, diagrams are the lesson's
own. Narration is the lesson's text, cleaned up for speech.
"""

from __future__ import annotations

import re
from pathlib import Path

from components import card, checklist, code, esc, grid, terminal

REPO = Path(__file__).resolve().parent.parent
SENIOR, JUNIOR = "senior", "junior"
VOICES = {SENIOR: "Microsoft David Desktop", JUNIOR: "Microsoft Zira Desktop"}

# --------------------------------------------------------------------------------------------- markdown parsing
FENCE = re.compile(r"^(<!-- test[^>]*-->\n)?```(bash|text)\n(.*?)\n```", re.M | re.S)


def section(text: str, name: str, level: int = 2) -> str:
    """The body of the heading `name` (at `level`), up to the next heading of the same or a higher level.
    Lines inside fenced code blocks are never headings (outputs can contain "# Cafe")."""
    out, inside, fence = [], False, False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            fence = not fence
        heading = None if fence or ln.startswith("```") else re_heading(ln)
        if heading and heading[0] <= level:
            if inside:
                break
            inside = heading[0] == level and heading[1] == name
            continue
        if inside:
            out.append(ln)
    return "\n".join(out).strip()


def re_heading(ln: str):
    m = re.match(r"^(#{1,6}) (.+?)\s*$", ln)
    return (len(m.group(1)), m.group(2)) if m else None


def items(md: str) -> list[tuple[str, str]]:
    """The section as a sequence of ("prose", text) / ("bash", code) / ("output", text), in order."""
    out, pos = [], 0
    md = re.sub(r"<details>.*?</details>", "", md, flags=re.S)
    for m in FENCE.finditer(md):
        prose = re.sub(r"<!--.*?-->", "", md[pos:m.start()]).strip()
        if prose:
            out.append(("prose", prose))
        out.append(("bash" if m.group(2) == "bash" else "output", m.group(3)))
        pos = m.end()
    rest = re.sub(r"<!--.*?-->", "", md[pos:]).strip()
    if rest:
        out.append(("prose", rest))
    return out


def runs(md: str) -> list[dict]:
    """Bash blocks with the prose before them and their recorded output (if any)."""
    seq, result, prose = items(md), [], ""
    for i, (kind, text) in enumerate(seq):
        if kind == "prose":
            prose = text
        elif kind == "bash":
            out = seq[i + 1][1] if i + 1 < len(seq) and seq[i + 1][0] == "output" else ""
            after = seq[i + 2][1] if i + 2 < len(seq) and seq[i + 2][0] == "prose" and out else (
                seq[i + 1][1] if i + 1 < len(seq) and seq[i + 1][0] == "prose" else "")
            result.append({"prose": prose, "bash": text, "out": out, "after": after})
            prose = ""
    return result


def first_prose(md: str) -> str:
    for kind, text in items(md):
        if kind == "prose":
            return text
    return ""


def visual(md: str) -> str:
    for kind, text in items(md):
        if kind == "output":          # the Visual section's ```text block
            return text
    return ""


def bullets(md: str) -> list[str]:
    return [re.sub(r"^\s*[-*]\s+", "", l).strip() for l in md.splitlines() if re.match(r"^\s*[-*]\s+", l)]


# --------------------------------------------------------------------------------------------- text for screen and speech
def plain(md: str) -> str:
    """Markdown → readable text (captions)."""
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"\1", t)
    t = t.replace("`", "")
    t = re.sub(r"^\s*[-*]\s+", "", t, flags=re.M)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def sentences(text: str, limit: int) -> str:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`(\"'])", text.strip())
    out = " ".join(parts[:limit]).strip()
    return out if out.endswith((".", "!", "?", ":")) else out + "."


def code_words(code_text: str) -> str:
    """Inline code read aloud: options without dashes, symbols as words."""
    t = code_text
    t = re.sub(r"HEAD~(\d+)", r"head tilde \1", t)
    t = re.sub(r"HEAD\^(\d)", r"head caret \1", t)
    t = re.sub(r"@\{(\w+)\}", r" at \1", t)
    t = re.sub(r"(?<!\w)--?([a-z])", r"\1", t)
    t = t.replace("...", " three dots ").replace("..", " two dots ")
    t = t.replace("/", " slash ").replace("~", "home ").replace("=", " equals ").replace("|", " pipe ")
    t = re.sub(r"[\"'<>{}\[\]()*]", " ", t)
    t = t.replace("-", " ").replace("_", " ").replace(":", " ")
    return re.sub(r"\s+", " ", t).strip()


SAY = [  # how the speech engine should say words it would otherwise mangle (captions keep the real spelling)
    (r"\bHEAD\b", "head"), (r"\bORIG_HEAD\b", "orig head"), (r"\bMERGE_HEAD\b", "merge head"),
    (r"\breflog\b", "ref log"), (r"\bREADME\b", "read me"), (r"\.gitignore\b", "dot git ignore"),
    (r"\bgitignore\b", "git ignore"), (r"\.gitattributes\b", "dot git attributes"), (r"\.gitmodules\b", "dot git modules"),
    (r"\.env\b", "dot env"), (r"\bGitHub\b", "git hub"), (r"\bGitLab\b", "git lab"), (r"\bgh\b", "G H"),
    (r"\bCI/CD\b", "C I C D"), (r"\bCI\b", "C I"), (r"\bCD\b", "C D"), (r"\bPRs\b", "P Rs"), (r"\bPR\b", "P R"),
    (r"\bGHCR\b", "G H C R"), (r"\bYAML\b", "yammel"), (r"\.yaml\b", " dot yammel"), (r"\.yml\b", " dot yammel"),
    (r"\bJSON\b", "jason"), (r"\.json\b", " dot jason"), (r"\.txt\b", " dot text"), (r"\.md\b", " dot M D"),
    (r"\.sh\b", " dot S H"), (r"\bSHA\b", "shah"), (r"\bSHA-256\b", "shah 256"), (r"\bSSH\b", "S S H"),
    (r"\bHTTPS\b", "H T T P S"), (r"\bHTTP\b", "H T T P"), (r"\bURLs?\b", "U R L"), (r"\bAPI\b", "A P I"),
    (r"\bCLI\b", "C L I"), (r"\bGPG\b", "G P G"), (r"\bLFS\b", "L F S"), (r"\bID\b", "I D"), (r"\bIDs\b", "I Ds"),
    (r"\bOS\b", "O S"), (r"\bOAuth\b", "oh auth"), (r"\bDevOps\b", "dev ops"), (r"\bGitOps\b", "git ops"),
    (r"\bkubectl\b", "kube control"), (r"\bkind\b", "kind"), (r"\bnginx\b", "engine x"), (r"\bHelm\b", "helm"),
    (r"\bsemver\b", "sem ver"), (r"\bvs\.?\b", "versus"), (r"\be\.g\.", "for example"), (r"\bi\.e\.", "that is"),
    (r"\bstdin\b", "standard in"), (r"\bstdout\b", "standard out"), (r"\bstderr\b", "standard error"),
    (r"\bcat-file\b", "cat file"), (r"\bfilter-repo\b", "filter repo"), (r"\bfsck\b", "F S check"),
    (r"\brerere\b", "re re re"), (r"\bzdiff3\b", "Z diff 3"), (r"\bdiff3\b", "diff 3"), (r"\bAKIA\b", "A K I A"),
    (r"\bTODO\b", "to do"), (r"\bWIP\b", "work in progress"), (r"\bOIDC\b", "O I D C"), (r"\b2FA\b", "two factor"),
    (r"\bCODEOWNERS\b", "code owners"), (r"\bmacOS\b", "mac O S"), (r"\bUbuntu\b", "oo-boon-too"),
    (r"\bv(\d+)\.(\d+)\.(\d+)\b", r"version \1 point \2 point \3"), (r"\bpatch-id\b", "patch I D"),
    (r"→", " to "), (r"≠", " not "), (r"…", "."), (r"·", ","), (r"—|–", ", "), (r"\s&\s", " and "),
]


def speech(md: str) -> str:
    t = re.sub(r"`([^`]+)`", lambda m: code_words(m.group(1)), md)
    t = plain(t)
    for pattern, repl in SAY:
        t = re.sub(pattern, repl, t)
    return re.sub(r"\s+", " ", t).strip()


def step(who: str, md: str, limit: int = 2, sfx: str | None = None, zoom: float = 1, hold: float = 0) -> dict:
    text = sentences(plain(md), limit) if md else ""
    spoken = sentences(speech(md), limit) if md else ""
    return {"say": text, "tts": spoken, "hl": None, "zoom": zoom, "sfx": sfx, "voice": VOICES[who], "who": who,
            "hold": hold}


def line(who: str, text: str, sfx: str | None = None) -> dict:
    return step(who, text, limit=9, sfx=sfx)


# --------------------------------------------------------------------------------------------- terminal content
def classify(text: str) -> str:
    low = text.lower()
    if re.search(r"\b(fatal|error|conflict|rejected|failed|fail |missing|denied|refusing|not possible|cannot)\b", low):
        return "bad"
    if re.search(r"\b(successfully|ok |all checks passed|deployed|merged|fast-forward|complete|good \")", low):
        return "ok"
    if low.startswith(("hint:", "warning:")):
        return "dim"
    return ""


def term_lines(run: dict, s: int, max_out: int = 14) -> list[tuple[int, str, str]]:
    lines = []
    for raw in run["bash"].splitlines():
        if not raw.strip():
            continue
        lines.append((s, ("  " if raw.startswith(" ") else "$ ") + raw.rstrip() if not raw.lstrip().startswith("#")
                      else raw.rstrip(), "dim" if raw.lstrip().startswith("#") else "cmd"))
    out = [l for l in run["out"].splitlines()]
    if len(out) > max_out:
        out = out[:max_out - 1] + [f"… ({len(out) - max_out + 1} more lines)"]
    lines += [(s, l, classify(l)) for l in out]
    return lines


def fits(lines: list[tuple[int, str, str]], limit: int = 21) -> list[tuple[int, str, str]]:
    """Keep the terminal readable: drop the oldest steps' lines when the panel would overflow."""
    while len(lines) > limit:
        first = lines[0][0]
        rest = [l for l in lines if l[0] != first]
        if not rest:
            return lines[-limit:]
        lines = rest
    return lines


# --------------------------------------------------------------------------------------------- scenes
QUESTIONS = ["Can you show me {t}?", "I keep hearing about {t}. What is it, really?", "How does {t} work?",
             "Why would I need {t}?", "What should I know about {t}?"]


def question(title: str, n: int) -> str:
    if re.match(r"(What|How|Why|When) ", title):
        return title.rstrip("?") + "?"
    topic = title[0].lower() + title[1:] if not title.startswith(("git ", "Git", "GitHub", "HEAD", "SSH", "HTTPS")) else title
    return QUESTIONS[n % len(QUESTIONS)].format(t=topic)


def visual_panel(text: str, title: str = "visual") -> str:
    longest = max((len(l) for l in text.splitlines()), default=40)
    rows = len(text.splitlines())
    size = max(15, min(26, int(1680 / (longest * 0.62)), int(660 / (rows * 1.5))))
    return code(title, text, lang="text", size=size)


def lesson_scenes(readme: Path, n: int, module: str) -> list[dict]:
    text = readme.read_text(encoding="utf-8")
    title = re.match(r"# Lesson (\d+) · (.+)", text).group(2).strip()
    number = re.match(r"# Lesson (\d+)", text).group(1)
    kicker = f"{module} · Lesson {number}"
    scenes = []

    # 1 · concept
    concept = first_prose(section(text, "What are we learning?"))
    vis = visual(section(text, "Visual"))
    body = visual_panel(vis) if vis else grid([card(1, "💡", title, esc(plain(concept)), "blue")], cols=1)
    scenes.append({"chapter": f"Lesson {number} · {title}", "kicker": kicker, "title": esc(title), "body": body,
                   "layout": "full",
                   "steps": [line(JUNIOR, question(title, n)), step(SENIOR, concept, 3)]})

    # 2 · demonstration (lab + the first demonstration blocks with their real output)
    lab = runs(section(text, "Lab setup"))
    demo = [r for r in runs(section(text, "Demonstration"))][:3]
    if demo:
        steps, lines = [], []
        if lab:
            steps.append(line(SENIOR, "First, a fresh practice repository for this lesson."))
            lines += term_lines(lab[0], 0, max_out=6)
        for r in demo:
            k = len(steps)
            narr = r["prose"] or r["after"] or "Let's run it."
            if r["after"] and r["out"]:
                narr = (r["prose"] + " " + r["after"]) if r["prose"] else r["after"]
            steps.append(step(SENIOR, narr, 2))
            lines += term_lines(r, k)
        scenes.append({"chapter": None, "kicker": kicker, "title": "Let's run it", "layout": "full",
                       "body": terminal(fits(lines), f"~/git-practice · lesson {number}"), "steps": steps})

    # 3 · break it (the junior's mistake) + troubleshoot
    brk = runs(section(text, "Break it"))
    trouble = section(text, "Troubleshoot")
    if brk:
        r = brk[0]
        intro = r["prose"] or first_prose(section(text, "Break it"))
        lines = term_lines(r, 0)
        steps = [step(JUNIOR, "Let me try something. " + intro, 2, sfx="error")]
        tr = runs(trouble)
        if tr and tr[0]["out"]:
            lines += term_lines(tr[0], 1, max_out=8)
        steps.append(step(SENIOR, first_prose(trouble) or "Look at the message: it tells you what went wrong.", 3))
        scenes.append({"chapter": None, "kicker": kicker, "title": "Break it, on purpose", "layout": "full",
                       "body": terminal(fits(lines), "~/git-practice · the mistake"), "steps": steps})

    # 4 · fix
    fix = runs(section(text, "Fix"))
    if fix:
        r = fix[0]
        narr = r["prose"] or first_prose(section(text, "Fix")) or "Here is the fix."
        scenes.append({"chapter": None, "kicker": kicker, "title": "Fix it", "layout": "full",
                       "body": terminal(fits(term_lines(r, 0)), "~/git-practice · the fix"),
                       "steps": [step(SENIOR, narr, 2, sfx="success")]})

    # 5 · recap
    rec = bullets(section(text, "Recap"))[:3]
    if rec:
        items_ = [(k + 1, esc(plain(b).split(":")[0] if len(plain(b)) > 70 and ":" in plain(b) else plain(b)), "")
                  for k, b in enumerate(rec)]
        steps = [line(JUNIOR, "Got it. What do I need to remember?")] + [step(SENIOR, b, 2) for b in rec]
        scenes.append({"chapter": None, "kicker": kicker, "title": "Remember", "layout": "full",
                       "body": checklist(items_), "steps": steps})
    return scenes


def module_parts() -> list[dict]:
    """One entry per video: number, slug, title, subtitle, files."""
    parts = []
    for mod in sorted(p for p in REPO.glob("[0-2][0-9]-*") if list(p.glob("[0-9][0-9]-*/README.md"))):
        readme = (mod / "README.md").read_text(encoding="utf-8")
        name = re.search(r"^# Module \d+ · (.+)$", readme, re.M).group(1)
        lessons = sorted(mod.glob("[0-9][0-9]-*/README.md"))
        first = re.match(r"# Lesson (\d+)", lessons[0].read_text(encoding="utf-8")).group(1)
        last = re.match(r"# Lesson (\d+)", lessons[-1].read_text(encoding="utf-8")).group(1)
        parts.append({"part": int(mod.name[:2]), "slug": mod.name, "title": f"Module {mod.name[:2]} · {name}",
                      "subtitle": f"Lessons {int(first)}–{int(last)}", "kind": "module", "files": lessons})
    parts.append({"part": 21, "slug": "21-devops-workflow", "title": "Module 21 · The DevOps workflow",
                  "subtitle": "From a branch to production", "kind": "workflow",
                  "files": [REPO / "21-devops-workflow/README.md"]})
    parts.append({"part": 22, "slug": "22-troubleshooting", "title": "Module 22 · Real-world troubleshooting",
                  "subtitle": "18 problems, solved step by step", "kind": "troubleshooting",
                  "files": sorted((REPO / "22-troubleshooting").glob("problem-*.md"))})
    parts.append({"part": 23, "slug": "24-capstone", "title": "Capstone · A broken repository to Kubernetes",
                  "subtitle": "The full chain, on GitHub", "kind": "capstone",
                  "files": [REPO / "24-capstone/walkthrough.md"]})
    return parts


def workflow_scenes(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    kicker = "Module 21 · DevOps workflow"
    vis = visual(section(text, "Visual"))
    scenes = [{"chapter": "The workflow", "kicker": kicker, "title": "Developer to deployment", "layout": "full",
               "body": visual_panel(vis), "steps": [
                   line(JUNIOR, "How does a change really get from my laptop to production?"),
                   step(SENIOR, first_prose(section(text, "What are we learning?")), 3)]}]
    demo = section(text, "Demonstration")
    for sub in re.findall(r"^### (.+)$", demo, re.M):
        body = section(demo, sub, level=3)
        rs = runs(body)
        if not rs:
            continue
        lines, steps = [], []
        for r in rs[:2]:
            k = len(steps)
            steps.append(step(SENIOR, r["prose"] or r["after"] or sub, 2))
            lines += term_lines(r, k)
        title = re.sub(r"^\d+\.\s*", "", sub)
        scenes.append({"chapter": title.split(" →")[0][:60], "kicker": kicker, "title": esc(title), "layout": "full",
                       "body": terminal(fits(lines), "~/git-practice/devops"), "steps": steps})
    brk, fix = runs(section(text, "Break it")), runs(section(text, "Fix"))
    if brk:
        scenes.append({"chapter": "When CI catches a mistake", "kicker": kicker, "title": "The pull request goes red",
                       "layout": "full", "body": terminal(fits(term_lines(brk[0], 0)), "the reviewer's clone"),
                       "steps": [step(JUNIOR, "Let me try something. " + brk[0]["prose"], 2, sfx="error"),
                                 step(SENIOR, first_prose(section(text, "Troubleshoot")), 3)]})
    if fix:
        scenes.append({"chapter": None, "kicker": kicker, "title": "Fixed, merged, released, deployed", "layout": "full",
                       "body": terminal(fits(term_lines(fix[0], 0, max_out=6)), "~/git-practice/devops"),
                       "steps": [step(SENIOR, fix[0]["prose"], 2, sfx="success")]})
    rec = bullets(section(text, "Recap"))
    scenes.append({"chapter": "Recap", "kicker": kicker, "title": "Remember", "layout": "full",
                   "body": checklist([(k + 1, esc(plain(b)), "") for k, b in enumerate(rec)]),
                   "steps": [line(JUNIOR, "So what is the shape of it?")] + [step(SENIOR, b, 2) for b in rec]})
    return scenes


def troubleshooting_scenes(path: Path, n: int) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    title = re.match(r"# Problem (\d+) · (.+)", text)
    number, name = title.group(1), title.group(2)
    kicker = f"Troubleshooting · Problem {number}"
    sym = runs(section(text, "Symptoms")) or runs(section(text, "Problem"))
    inv = runs(section(text, "Investigation"))
    fix = runs(section(text, "Fix"))
    lines, steps = [], [step(JUNIOR, first_prose(section(text, "Problem")), 2, sfx="error")]
    if sym:
        lines += term_lines(sym[-1], 0, max_out=8)
    if inv:
        steps.append(step(SENIOR, inv[0]["prose"] or first_prose(section(text, "Investigation")), 2))
        lines += term_lines(inv[0], 1, max_out=8)
    steps.append(step(SENIOR, first_prose(section(text, "Root cause")), 2))
    scenes = [{"chapter": f"{number} · {name}", "kicker": kicker, "title": esc(name), "layout": "full",
               "body": terminal(fits(lines), "~/git-practice · investigate"), "steps": steps}]
    if fix:
        pv = bullets(section(text, "Prevention"))[:2]
        scenes.append({"chapter": None, "kicker": kicker, "title": "Fix and prevent", "layout": "full",
                       "body": terminal(fits(term_lines(fix[0], 0, max_out=10)), "~/git-practice · fix"),
                       "steps": [step(SENIOR, fix[0]["prose"] or first_prose(section(text, "Fix")), 2, sfx="success")]
                       + [step(SENIOR, p, 1) for p in pv]})
    return scenes


def capstone_scenes(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    kicker = "Capstone"
    challenge = (REPO / "24-capstone/README.md").read_text(encoding="utf-8")
    vis = visual(section(challenge, "The challenge"))
    scenes = [{"chapter": "The challenge", "kicker": kicker, "title": "A broken repository", "layout": "full",
               "body": visual_panel(vis, "the goal"),
               "steps": [line(JUNIOR, "The team left us a mess. Where do we even begin?"),
                         step(SENIOR, first_prose(section(challenge, "The challenge")), 3)]}]
    for part in ("Part 1 · Repair the repository locally", "Part 2 · Publish, protect, review, release, deploy"):
        body = section(text, part)
        for sub in re.findall(r"^### (.+)$", body, re.M):
            rs = [r for r in runs(section(body, sub, level=3)) if r["out"]]
            if not rs:
                continue
            r = rs[0]
            title = re.sub(r"^\d+\.\s*", "", sub)
            sfx = "success" if re.search(r"success|complete|Successfully|passed|Merged|new tag", r["out"]) else None
            sfx = "error" if re.search(r"MISSING|FAIL|GH006", r["out"]) else sfx
            scenes.append({"chapter": title[:60], "kicker": f"{kicker} · {part.split(' · ')[0]}", "title": esc(title),
                           "layout": "full", "body": terminal(fits(term_lines(r, 0, max_out=16)), "~/git-practice/capstone"),
                           "steps": [step(SENIOR, r["prose"] or r["after"] or title, 2, sfx=sfx)]})
    return scenes


def build(part: int) -> tuple[dict, list[dict]]:
    info = next(p for p in module_parts() if p["part"] == part)
    scenes: list[dict] = []
    if info["kind"] == "module":
        for n, f in enumerate(info["files"]):
            scenes += lesson_scenes(f, n, info["title"].split(" · ")[0])
    elif info["kind"] == "workflow":
        scenes = workflow_scenes(info["files"][0])
    elif info["kind"] == "troubleshooting":
        for n, f in enumerate(info["files"]):
            scenes += troubleshooting_scenes(f, n)
    else:
        scenes = capstone_scenes(info["files"][0])
    return info, scenes


if __name__ == "__main__":
    import sys
    for p in module_parts():
        if len(sys.argv) > 1 and str(p["part"]) not in sys.argv[1:]:
            continue
        info, scenes = build(p["part"])
        words = sum(len(s["say"].split()) for sc in scenes for s in sc["steps"])
        print(f"{p['part']:02d} {info['title']:<50} {len(scenes):3d} scenes {words:5d} words ≈ {words / 150:4.1f} min")
