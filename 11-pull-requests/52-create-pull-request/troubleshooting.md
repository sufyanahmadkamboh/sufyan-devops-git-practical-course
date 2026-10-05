<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 52 · Creating a pull request · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Run `gh pr create` again for the same branch:

```bash
gh pr create --base main --head add-green-tea --title "Add green tea" --body "again" 2>&1
```

```text
a pull request for branch "add-green-tea" into branch "main" already exists:
https://github.com/sufyanahmadkamboh/git-practice-cafe/pull/8
```

## Troubleshoot

A branch can have only one open PR into the same base. The second one is unnecessary: pushing to the branch already
updated the existing PR. If the title or description needs to change, edit the PR instead of opening a new one.

## Fix

```bash
gh pr edit add-green-tea --title "Green tea: menu and price" > /dev/null
gh pr view add-green-tea --json title --jq .title
```

```text
Green tea: menu and price
```
