<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 09 · git add · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Stage the extra `chai` line too, but use a dry run first to check what `git add` would do.

**Expected result.** The dry run lists `add 'menu.txt'`; afterwards `menu.txt` shows `M ` (fully staged).

**Verification.**

```bash
cd ~/git-practice/lesson-09
git add -n .
git status --short
```
