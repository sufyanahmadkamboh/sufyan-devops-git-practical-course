<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 15 · git diff · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show the price change with `--word-diff` so only the changed number is highlighted.

**Expected result.** `latte [-3.20-]{+3.30+}`.

**Verification.**

```bash
cd ~/git-practice/lesson-15
git diff --word-diff prices.txt
```
