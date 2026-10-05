"""Generate each lesson's companion files from its README.md.

Every lesson is written once, in README.md, with these sections (among others):

    ## Hands-on exercise   -> exercise.md
    ## Practice challenge  -> challenge.md
    ## Break it, ## Troubleshoot, ## Fix  -> troubleshooting.md
    every ```bash block, under its section title -> commands.md

    python tools/lesson_files.py            write the files
    python tools/lesson_files.py --check    fail if any file is missing or out of date (CI)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = sorted(ROOT.glob("[0-2][0-9]-*/[0-9][0-9]-*/README.md"))
HEADER = "<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->\n"


def sections(text: str) -> list[tuple[str, str]]:
    """(title, body) for every '## ' section, in order."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def strip_tests(body: str) -> str:
    """Test annotations are for the runner; the companion files are for reading."""
    body = re.sub(r"^<!-- test(-run)?:.*-->\n\n?", "", body, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"


def relink(body: str) -> str:
    """Links in README.md are relative to the lesson folder, and so are the companion files: nothing to change,
    except links to README.md sections, which now point back to the README."""
    return re.sub(r"\]\(#([^)]+)\)", r"](README.md#\1)", body)


def build(readme: Path) -> dict[str, str]:
    text = readme.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    secs = dict(sections(text))
    out = {}

    def page(kind: str, names: list[str]) -> str | None:
        found = [(n, secs[n]) for n in names if n in secs]
        if not found:
            return None
        body = "".join(f"## {n}\n\n{relink(strip_tests(b))}\n" for n, b in found)
        return f"{HEADER}# {title} · {kind}\n\n> The full lesson: [README.md](README.md)\n\n{body}".rstrip() + "\n"

    for name, kind, names in [
        ("exercise.md", "exercise", ["Hands-on exercise"]),
        ("challenge.md", "challenge", ["Practice challenge"]),
        ("troubleshooting.md", "troubleshooting", ["Break it", "Troubleshoot", "Fix"]),
    ]:
        content = page(kind, names)
        if content is None:
            raise SystemExit(f"{readme.relative_to(ROOT)}: missing section for {name}")
        out[name] = content

    cmds = []
    for sec, body in sections(text):
        blocks = re.findall(r"^```bash\n(.*?)^```", body, flags=re.M | re.S)
        if blocks:
            cmds.append(f"## {sec}\n\n" + "\n".join(f"```bash\n{b}```\n" for b in blocks))
    out["commands.md"] = f"{HEADER}# {title} · commands\n\n> Every command of the lesson, in order. The explanations: [README.md](README.md)\n\n" \
        + "\n".join(cmds)
    return out


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for readme in LESSONS:
        for name, content in build(readme).items():
            target = readme.parent / name
            if check:
                if not target.exists() or target.read_text(encoding="utf-8") != content:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.write_text(content, encoding="utf-8", newline="\n")
    if check and stale:
        print("out of date (run python tools/lesson_files.py):\n  " + "\n  ".join(stale))
        return 1
    print(f"{len(LESSONS)} lessons {'checked' if check else 'written'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
