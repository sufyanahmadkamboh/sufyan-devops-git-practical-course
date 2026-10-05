<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 33 · git reflog · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Using the reflog of the branch `main` (not of HEAD), find the commit `main` pointed to before the
reset, and create a branch `rescue` there.

**Expected result.** `rescue` points to "Price mocha".

**Verification.**

```bash
cd ~/git-practice/lesson-33
git reflog show main | head -3
git log --oneline -1 rescue
```
