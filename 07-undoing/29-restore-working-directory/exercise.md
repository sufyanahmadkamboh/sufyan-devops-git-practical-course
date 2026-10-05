<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 29 · Undo working directory changes · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Bring `prices.txt` back to how it was in the **first** commit that contained it, using `--source`.

**Expected result.** The file matches the commit `Add prices`, and `git status` shows it modified (if it differs) or
clean (if it is identical, as here).

**Verification.**

```bash
cd ~/git-practice/lesson-29
git restore --source=4267004 prices.txt
cat prices.txt
```
