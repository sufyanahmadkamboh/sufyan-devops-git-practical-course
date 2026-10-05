<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 63 · Interactive rebase · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** `drop` the commit "Add mocha with its price" from the history.

**Expected result.** No mocha in `menu.txt` or `prices.txt`; the green tea commit is the newest.

**Verification.**

```bash
cd ~/git-practice/lesson-63
cat menu.txt prices.txt
git log --oneline -2
```
