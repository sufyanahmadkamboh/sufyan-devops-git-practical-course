<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 94 · Labels · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

A typo in the label name:

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:hihg" 2>&1
```

```text
failed to update https://github.com/sufyanahmadkamboh/git-practice-cafe/issues/41: 'priority:hihg' not found
failed to update 1 issue
```

## Troubleshoot

`'priority:hihg' not found`: labels must exist in the repository before they can be applied (the web interface only
offers existing ones; the CLI and API refuse unknown names). Check the exact spelling:

```bash
gh label list --json name --jq '.[] | select(.name | startswith("priority")) | .name'
```

## Fix

```bash
n=$(gh issue list --state open --json number,title --jq '[.[] | select(.title | startswith("Espresso is charged"))][0].number')
gh issue edit "$n" --add-label "priority:high" > /dev/null
gh issue view "$n" --json labels --jq '[.labels[].name] | join(", ")'
```

```text
bug, good first issue, priority:high, area:prices
```
