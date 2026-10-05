<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 67 · Cherry-pick · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Find the commits on `feature-specials` that production does **not** have an equivalent of
(`git cherry`).

**Expected result.** Two `+` lines (the specials commits) and one `-` line (the fix, already applied).

**Verification.**

```bash
cd ~/git-practice/lesson-67
git cherry -v production feature-specials
```
