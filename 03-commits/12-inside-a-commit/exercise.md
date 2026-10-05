<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 12 · What actually happens during a commit? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Print the first commit's parent list (it has none) and the latest commit's parent.

**Expected result.** The root commit `d6df412` has no parent; every other commit has one.

**Verification.**

```bash
cd ~/git-practice/lesson-12
git log --format='%h  parents: %p  %s'
```
