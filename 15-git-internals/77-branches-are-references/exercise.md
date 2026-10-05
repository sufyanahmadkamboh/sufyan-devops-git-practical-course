<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 77 · Branches are references · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Move `experiment` to `main`'s commit with `update-ref`, then list branches pointing at the same
commit as `main`.

**Expected result.** `experiment` and `main`.

**Verification.**

```bash
cd ~/git-practice/lesson-77
git branch --points-at main
```
