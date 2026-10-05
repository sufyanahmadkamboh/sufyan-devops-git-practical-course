<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 18 · Creating branches · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Two classic mistakes: a name that already exists, and an invalid name.

```bash
git branch hotfix-prices 2>&1
```

```text
fatal: a branch named 'hotfix-prices' already exists
```

```bash
git branch "fix prices" 2>&1
```

```text
fatal: 'fix prices' is not a valid branch name
hint: See 'git help check-ref-format'
hint: Disable this message with "git config set advice.refSyntax false"
```

## Troubleshoot

`a branch named 'hotfix-prices' already exists`: names are unique. `'fix prices' is not a valid branch name`: no
spaces, no `..`, no `~ ^ : ? * [` or ending in `.lock`. Check a name before using it:

```bash
git check-ref-format --branch "fix-prices"
```

## Fix

```bash
git branch fix-prices
git branch
```
