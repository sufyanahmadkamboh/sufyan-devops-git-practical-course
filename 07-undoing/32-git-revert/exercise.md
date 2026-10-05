<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 32 · git revert · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Revert the revert: the machine is repaired.

**Expected result.** `mocha` is back in `menu.txt`, and the history shows both reverts.

**Verification.**

```bash
cd ~/git-practice/lesson-32
grep mocha menu.txt
git log --oneline -2
```
