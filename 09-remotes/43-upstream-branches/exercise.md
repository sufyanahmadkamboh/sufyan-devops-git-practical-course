<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 43 · Upstream branches · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Using `@{u}`, list the commits on `feature-chai` that are not pushed yet.

**Expected result.** `Price chai`.

**Verification.**

```bash
cd ~/git-practice/lesson-43/ada
git log --oneline '@{u}..'
```
