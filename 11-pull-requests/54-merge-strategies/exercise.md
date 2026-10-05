<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 54 · Merge strategies · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** On `main-squash`, find which PR branch commits are **not** on `main-squash` according to Git.

**Expected result.** Both `pr-squash` commits: squashing created a new commit, so Git does not consider them merged.

**Verification.**

```bash
cd ~/git-practice/lesson-54
git log --oneline main-squash..pr-squash
```
