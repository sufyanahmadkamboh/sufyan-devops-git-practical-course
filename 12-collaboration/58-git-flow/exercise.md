<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 58 · Git Flow · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the tags and the commit each one points to.

**Expected result.** `v1.0.0` and `v1.1.0`.

**Verification.**

```bash
cd ~/git-practice/lesson-58
git tag -n --format='%(refname:short) %(*objectname:short) %(contents:subject)'
```
