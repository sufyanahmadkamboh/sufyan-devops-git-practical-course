<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 26 · Merge conflicts · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Find out from Git (not by reading the file) which files are in conflict.

**Expected result.** `prices.txt`.

**Verification.**

```bash
cd ~/git-practice/lesson-26
git diff --name-only --diff-filter=U
```
