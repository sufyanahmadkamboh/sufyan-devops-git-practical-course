<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 01 · What is Git? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** In `~/git-practice/lesson-01/with-git`, add a fourth version: put `mocha 3.90` in `prices.txt` and
commit it with the message `Add mocha`.

**Expected result.** `git log --oneline` shows four commits, the newest on top.

**Verification.**

```bash
cd ~/git-practice/lesson-01/with-git
git log --oneline | head -1
git log --oneline | wc -l
```
