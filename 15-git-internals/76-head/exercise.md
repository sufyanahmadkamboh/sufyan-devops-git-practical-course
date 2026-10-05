<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 76 · HEAD · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Print the subject of the commit two before `HEAD`, using `HEAD~2`.

**Expected result.** "Add prices".

**Verification.**

```bash
cd ~/git-practice/lesson-76
git log -1 --format=%s HEAD~2
```
