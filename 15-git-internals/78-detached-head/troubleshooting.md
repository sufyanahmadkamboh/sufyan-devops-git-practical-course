<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 78 · Detached HEAD · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Make a hotfix commit while detached, then switch back to `main`:

```bash
sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix: espresso price"
git switch main 2>&1
```

```text
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  706d7af Hotfix: espresso price

If you want to keep it by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> 706d7af

Switched to branch 'main'
```

## Troubleshoot

Git warns: the commit is not connected to any branch, so no branch log shows it and garbage collection will eventually
delete it. The warning even prints the command to keep it. If the terminal output is gone, the reflog still has it:

```bash
git reflog | grep -m1 "Hotfix"
```

```text
706d7af HEAD@{1}: commit: Hotfix: espresso price
```

## Fix

```bash
git branch hotfix-espresso "$(git reflog --format=%h --grep-reflog='commit: Hotfix' | head -1)"
git log --oneline -1 hotfix-espresso
```

```text
706d7af (hotfix-espresso) Hotfix: espresso price
```
