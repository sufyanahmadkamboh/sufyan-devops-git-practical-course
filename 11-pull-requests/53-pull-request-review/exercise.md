<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 53 · Pull request review · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List every line comment of the PR with its file and line.

**Expected result.** `prices.txt:4 …`.

**Verification.**

```bash
me=$(gh api user --jq .login)
number=$(gh pr view price-green-tea --json number --jq .number)
gh api "repos/$me/git-practice-cafe/pulls/$number/comments" --jq '.[] | "\(.path):\(.original_line) \(.user.login)"'
```
