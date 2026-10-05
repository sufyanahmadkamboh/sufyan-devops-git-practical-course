<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 33 · git reflog · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Delete a branch with unmerged work, a different way of "losing" commits:

```bash
git switch -q -c risky && echo "seasonal: pumpkin latte" >> menu.txt && git commit -q -am "Add pumpkin latte"
git switch -q main
git branch -D risky
```

```text
Deleted branch risky (was c384746).
```

## Troubleshoot

`Deleted branch risky (was ...)`: Git even printed the commit ID. If the terminal output is gone, the reflog still
has the commit, as the last position of HEAD on that branch:

```bash
git reflog | grep -m1 "pumpkin"
```

```text
c384746 HEAD@{1}: commit: Add pumpkin latte
```

## Fix

```bash
lost=$(git reflog --format=%h --grep-reflog="commit: Add pumpkin latte" | head -1)
git branch risky "$lost"
git log --oneline -1 risky
```

```text
c384746 (risky) Add pumpkin latte
```
