<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 82 · What are Git hooks? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Run the post-commit hook by hand, without committing.

**Expected result.** A second line in `.git/commit-log.txt` (the same commit again).

**Verification.**

```bash
cd ~/git-practice/lesson-82
wc -l < .git/commit-log.txt
```
