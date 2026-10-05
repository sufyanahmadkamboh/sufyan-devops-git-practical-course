<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 11 · git commit · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Commit `specials.txt` with a summary and a body explaining why.

**Expected result.** `git log -1` shows both paragraphs; `git status` is clean.

**Verification.**

```bash
cd ~/git-practice/lesson-11
git log -1 --format='%s%n%n%b'
git status --short
```
