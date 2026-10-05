<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 10 · The staging area · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Change both `prices.txt` (raise the espresso to 2.60) and `menu.txt` (add `chai`). Stage only the
price change, and prove with the two diffs which change will be committed.

**Expected result.** `git diff --staged` shows only `espresso`; `git diff` shows only `chai`.

**Verification.**

```bash
cd ~/git-practice/lesson-10
git diff --staged | grep '^[+-][a-z]'
git diff | grep '^[+-][a-z]'
```
