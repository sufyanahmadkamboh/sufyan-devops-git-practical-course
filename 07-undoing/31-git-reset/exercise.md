<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 31 · git reset: soft, mixed and hard · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Squash the last two commits ("Add green tea", "Price green tea") into one using `--soft`.

**Expected result.** One commit "Add green tea with its price" containing both changes.

**Verification.**

```bash
cd ~/git-practice/lesson-31
git show --stat --format=%s HEAD
```
