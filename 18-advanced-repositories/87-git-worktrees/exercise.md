<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 87 · Git worktrees · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Merge the hotfix into `main` from the main worktree... `main` is not checked out anywhere, so do it
from the hotfix worktree: switch it to `main` and merge.

**Expected result.** `main` contains "Fix the espresso price".

**Verification.**

```bash
cd ~/git-practice/lesson-87
git log --oneline -1 main
```
