<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 44 · What is GitHub? · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Find out how many branches the `octocat/Hello-World` repository has, without cloning.

**Expected result.** The number of `refs/heads/` lines.

**Verification.**

```bash
git ls-remote --heads https://github.com/octocat/Hello-World | wc -l
```
