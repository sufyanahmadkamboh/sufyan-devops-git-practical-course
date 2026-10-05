<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 13 · git log · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the commits on `feature-tea` that are not on `main`.

**Expected result.** Exactly one commit: `Add matcha`.

**Verification.**

```bash
cd ~/git-practice/lesson-13
git log --oneline main..feature-tea
```

`A..B` means "reachable from B but not from A": what B has that A does not.
