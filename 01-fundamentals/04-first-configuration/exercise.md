<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 04 · First Git configuration · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** In the lab repository, remove the local e-mail so the global one applies again.

**Expected result.** `git config user.email` prints `ada@example.com`, with scope `global`.

**Verification.**

```bash
cd ~/git-practice/lesson-04
git config --show-scope --get user.email
```
