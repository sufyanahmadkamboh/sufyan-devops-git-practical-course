<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 64 · Rebase conflicts · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Check that the rebased commit still carries its original message and author.

**Expected result.** "Raise the latte price to 3.50" by Ada Lovelace (although the price is now 3.40: consider
rewording it, lesson 63).

**Verification.**

```bash
cd ~/git-practice/lesson-64
git log -2 --format='%s by %an'
```
