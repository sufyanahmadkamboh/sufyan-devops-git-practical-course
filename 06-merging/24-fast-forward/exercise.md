<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 24 · Fast-forward merge · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Create a branch with one commit and merge it with `--ff-only`.

**Expected result.** `Fast-forward`, and no merge commit.

**Verification.**

```bash
cd ~/git-practice/lesson-24
git log --oneline -1
git log --oneline --merges | wc -l
```
