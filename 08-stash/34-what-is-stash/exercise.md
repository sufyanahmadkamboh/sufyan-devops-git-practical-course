<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 34 · What is a stash? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Stash your current work again, confirm the folder is clean, then pop it.

**Expected result.** After the stash: `git status` clean; after pop: `flat white` back in `menu.txt`.

**Verification.**

```bash
cd ~/git-practice/lesson-34
grep "flat white" menu.txt
git stash list | wc -l
```
