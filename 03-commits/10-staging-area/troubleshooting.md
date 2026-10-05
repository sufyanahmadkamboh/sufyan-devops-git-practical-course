<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 10 · The staging area · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Commit and expect everything to be in it, without checking:

```bash
git commit -q -m "Update espresso price and add chai"
git status --short
```

## Troubleshoot

The message says "and add chai" but `git status` still shows ` M menu.txt`: `chai` was never staged, so the commit
contains only the price. The commit message now lies about the commit.

```bash
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

```text
-espresso 2.50
+espresso 2.60
```

## Fix

The commit is not pushed, so it may be changed: stage the missing part and amend the last commit (lesson 11):

```bash
git add menu.txt
git commit -q --amend --no-edit
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

```text
+chai
-espresso 2.50
+espresso 2.60
```
