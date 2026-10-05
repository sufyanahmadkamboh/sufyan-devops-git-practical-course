<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 35 · Stash, apply and pop · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Change `menu.txt` and `prices.txt`, but stash only `menu.txt`.

**Expected result.** `prices.txt` stays modified in your folder; the stash contains only `menu.txt`.

**Verification.**

```bash
cd ~/git-practice/lesson-35
git status --short
git stash show --name-only
```
