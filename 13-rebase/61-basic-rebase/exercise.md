<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 61 · Basic rebase · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Create `feature-chai` from the commit **before** the last two, add a commit, and rebase it onto `main`.

**Expected result.** `feature-chai`'s commit sits on top of `main`.

**Verification.**

```bash
cd ~/git-practice/lesson-61
git rev-list --count feature-chai..main
git log --oneline -2 feature-chai
```
