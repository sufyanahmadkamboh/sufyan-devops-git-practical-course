<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 46 · Connecting local Git to GitHub · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Open the repository page and confirm the three files are there, using the CLI.

**Expected result.** `README.md`, `menu.txt`, `prices.txt`.

**Verification.**

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/contents" --jq '.[].name'
```
