<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 79 · Recover a deleted branch · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show that the server has `feature-hours` again, with both commits.

**Expected result.** `refs/heads/feature-hours` in `git ls-remote`, two commits after `main`.

**Verification.**

```bash
cd ~/git-practice/lesson-79/ada
git ls-remote --heads origin
git log --oneline main..feature-hours
```
