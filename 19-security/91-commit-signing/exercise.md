<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 91 · Commit signing · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Sign every commit automatically, make one more commit, and list the signature status of the last
three commits.

**Expected result.** `G` for the two signed commits, `N` for the unsigned "Add prices".

**Verification.**

```bash
cd ~/git-practice/lesson-91
git log --format='%G? %h %s' -3
```
