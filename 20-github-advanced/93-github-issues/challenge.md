<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 93 · GitHub Issues · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show the newest closed issue with each of the two titles, and how it was closed (`closedByPullRequestsReferences`
is empty here because the fixes were commits, not PRs).

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-93
gh issue list --state closed --limit 50 --json number,title,stateReason \
  --jq '[.[] | select(.title == "Green tea has no price" or .title == "Add chai to the menu")] | unique_by(.title)[] | "#\(.number) \(.title): \(.stateReason)"'
```

```text
#35 Add chai to the menu: COMPLETED
#34 Green tea has no price: COMPLETED
```

</details>
