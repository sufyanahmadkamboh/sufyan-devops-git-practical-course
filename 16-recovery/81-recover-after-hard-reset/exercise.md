<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 81 · Recover after a hard reset · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Before any risky operation, leave yourself a rescue point: create a branch `before-cleanup` at the
current commit, reset hard to `HEAD~1`, and verify the rescue branch still has "Price green tea".

**Expected result.** `before-cleanup` points to "Price green tea"; `main` to "Add green tea".

**Verification.**

```bash
cd ~/git-practice/lesson-81
git log --oneline -1 before-cleanup
git log --oneline -1 main
```
