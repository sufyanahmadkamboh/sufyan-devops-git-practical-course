<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 07 · The working directory · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Rename `README.md` to `INFO.md` with plain `mv` and look at `git status --short`.

**Expected result.** Git shows the old name as deleted and the new name as untracked. It recognises a rename only once
both sides are staged (lesson 09: `git add -A` then shows `R`).

**Verification.**

```bash
cd ~/git-practice/lesson-07
git status --short
```
