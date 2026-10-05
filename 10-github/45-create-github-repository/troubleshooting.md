<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 45 · Creating a GitHub repository · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Create it a second time:

```bash
gh repo create git-practice-cafe --public 2>&1
```

```text
GraphQL: Name already exists on this account (createRepository)
```

## Troubleshoot

`Name already exists on this account`: repository names are unique per owner. Either the repository is already there
(use it: `gh repo view git-practice-cafe`) or pick another name. Also check the **owner**: in an organisation, the same
name can exist under your personal account and under the organisation.

## Fix

Nothing to recreate: list your repositories and use the existing one.

```bash
gh repo list --limit 100 --json name --jq '.[].name' | grep -x git-practice-cafe
```
