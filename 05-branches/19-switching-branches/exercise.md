<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 19 · Switching branches · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Make an uncommitted change to `prices.txt`, switch to `feature-tea`, and check whether the change
came with you.

**Expected result.** The change follows you: `prices.txt` is modified on `feature-tea` too, because that file is the
same in both branches, so Git can keep your edit.

**Verification.**

```bash
cd ~/git-practice/lesson-19
git branch --show-current
git status --short
```
