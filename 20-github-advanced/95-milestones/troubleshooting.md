<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 95 · Milestones · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Assign an issue to a milestone that does not exist (the release was renamed):

```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1" 2>&1
```

```text
could not add to milestone 'v1.1': 'v1.1' not found
```

## Troubleshoot

`could not add to milestone 'v1.1': 'v1.1' not found`: milestones are matched by exact title. The issue was not created
(the command failed as a whole). List the existing ones:

```bash
me=$(gh api user --jq .login)
gh api "repos/$me/git-practice-cafe/milestones" --jq '.[].title'
```

## Fix

```bash
gh issue create --title "Seasonal drinks" --body "Ideas for winter." --milestone "v1.1.0"
```
