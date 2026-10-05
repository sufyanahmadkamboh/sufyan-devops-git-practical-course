<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 09 · git add · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Create two new files in a subfolder `docs/` and one modified file at the top level. From inside `docs/`, stage only
the two new files with one command, then stage everything with another.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-09
git add -A && git commit -q -m "Save the lesson's changes"
mkdir -p docs && echo "a" > docs/a.md && echo "b" > docs/b.md && echo "x" >> README.md
cd docs
git add .
git status --short
echo "---"
git add -A
git status --short
```

```text
 M ../README.md
A  a.md
A  b.md
---
M  ../README.md
A  a.md
A  b.md
```

From `docs/`, `git add .` staged only `docs/` (`README.md` one folder up stays ` M`); `git add -A` staged it
too. Paths in `git status` are shown relative to the folder you are in.

</details>
