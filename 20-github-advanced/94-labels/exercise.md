<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 94 · Labels · exercise

> The full lesson: [README.md](README.md)

## Hands-on exercise

**Instructions.** Add the label `good first issue` to the espresso issue, and list issues with that label.

**Expected result.** The espresso issue appears.

<!-- test-run github: cd ~/git-practice/lesson-94 && n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number') && gh issue edit "$n" --add-label "good first issue" > /dev/null -->

**Verification.**

```bash
cd ~/git-practice/lesson-94
gh issue list --label "good first issue" --json title --jq '.[].title'
```
