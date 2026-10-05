<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 41 · git pull · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Grace pushes another commit; pull it into Ada's clone with `--ff-only`.

**Expected result.** `Fast-forward`.

**Verification.**

```bash
cd ~/git-practice/lesson-41/ada
git pull --ff-only
git log --oneline -1
```
