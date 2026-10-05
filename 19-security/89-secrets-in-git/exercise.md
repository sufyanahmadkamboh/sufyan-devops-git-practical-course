<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 89 · Secrets in Git · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Search the entire history of the clone for anything that looks like a password assignment.

**Expected result.** The commit and line containing `DB_PASSWORD=`.

**Verification.**

```bash
cd ~/git-practice/lesson-89/eve
git grep -n "PASSWORD=" $(git rev-list --all) | head -3
```
