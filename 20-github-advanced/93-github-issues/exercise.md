<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 93 · GitHub Issues · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Open a second issue, "Add chai to the menu", comment on it, and view it with its comments.

**Expected result.** The issue with your comment.

<!-- test-run github: cd ~/git-practice/lesson-93 && gh issue create --title "Add chai to the menu" --body "Several customers asked for chai." > /dev/null && n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number') && gh issue comment "$n" --body "I will take this one." > /dev/null -->

**Verification.**

```bash
cd ~/git-practice/lesson-93
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title == "Add chai to the menu")][0].number')
gh issue view "$n" --comments | tail -4
```
