<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 98 · GitHub Actions introduction · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the last runs of the workflow with their commit titles and conclusions.

**Expected result.** The run for "ci: check the price file on every push" with `success`.

**Verification.**

```bash
cd ~/git-practice/lesson-98
gh run list --workflow check-prices --limit 3 --json displayTitle,conclusion --jq '.[] | "\(.conclusion) \(.displayTitle)"'
```
