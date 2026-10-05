<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 68 · Git tags · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the tags matching `v1.*` and show which commit `v0.9.0` points to.

**Expected result.** `v1.0.0`; `fc345e6 (tag: v0.9.0) Add the menu`.

**Verification.**

```bash
cd ~/git-practice/lesson-68/ada
git tag -l "v1.*"
git log --oneline -1 v0.9.0
```
