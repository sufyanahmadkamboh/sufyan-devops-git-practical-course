<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 95 · Milestones · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** List the open issues of the milestone.

**Expected result.** Only "Update the menu board".

**Verification.**

```bash
cd ~/git-practice/lesson-95
gh issue list --milestone "v1.1.0" --state open --json title --jq '.[].title'
```
