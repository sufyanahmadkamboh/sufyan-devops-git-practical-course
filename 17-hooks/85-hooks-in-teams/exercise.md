<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 85 · Git hooks in teams · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Commit Ada's change with a valid message and push it.

**Expected result.** `feat: add green tea` on the server.

**Verification.**

```bash
cd ~/git-practice/lesson-85
git --git-dir=server/cafe.git log --oneline -1
```
