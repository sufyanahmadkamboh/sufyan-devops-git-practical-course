<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 74 · How Git stores data · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Count the objects in the repository and explain the number: 3 commits, each with a tree, and how
many distinct blobs?

**Expected result.** `count: 9` loose objects (3 commits + 3 trees + 3 blobs: README, menu, prices).

**Verification.**

```bash
cd ~/git-practice/lesson-74
git count-objects -v | head -1
```
