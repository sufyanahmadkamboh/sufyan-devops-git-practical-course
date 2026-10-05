<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 45 · Creating a GitHub repository · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Show the repository's default branch name and whether it is empty.

**Expected result.** `isEmpty` is `true` until you push (lesson 46).

**Verification.**

```bash
gh repo view git-practice-cafe --json isEmpty,defaultBranchRef
```
