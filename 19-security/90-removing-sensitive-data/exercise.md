<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 90 · Removing sensitive data · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Verify on the **server** that no commit on any branch contains `.env`.

**Expected result.** `0`.

**Verification.**

```bash
cd ~/git-practice/lesson-90
git --git-dir=server/cafe.git log --all --oneline -- .env | wc -l
```
