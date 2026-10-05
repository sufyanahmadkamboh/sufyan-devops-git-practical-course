<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 21 · Branch visualization · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Find the commit where `main` and `feature` forked.

**Expected result.** `4267004`, the "Add prices" commit.

**Verification.**

```bash
cd ~/git-practice/lesson-21
git merge-base main feature | cut -c1-7
```
