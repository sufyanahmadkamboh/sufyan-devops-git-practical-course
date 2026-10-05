<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 17 · Why branches exist · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** In `lesson-17b`, finish the loyalty feature on its branch (remove `(WORK IN PROGRESS)`) without
touching `main`.

**Expected result.** `feature-loyalty` has two commits that `main` does not have; `main` is unchanged.

**Verification.**

```bash
cd ~/git-practice/lesson-17b
git log --oneline main..feature-loyalty
```
