# Problem 4 · Accidental reset

> Troubleshooting lab · run every command from the course folder · related lessons: [31](../07-undoing/31-git-reset/README.md), [33](../07-undoing/33-git-reflog/README.md), [81](../16-recovery/81-recover-after-hard-reset/README.md)

## Problem

Meaning to drop one commit, you ran `git reset --hard HEAD~3`: three commits are gone from the branch.

<!-- test: contains=lesson-t04 -->
```bash
bash scripts/new-lab.sh lesson-t04 history
cd ~/git-practice/lesson-t04
git reset -q --hard HEAD~3
```

## Symptoms

<!-- test: absent=mocha; output -->
```bash
git log --oneline -3
cat menu.txt
```

```text
6833580 (HEAD -> main) Add green tea
4267004 Add prices
fc345e6 Add the menu
espresso
latte
cappuccino
green tea
```

"Price green tea", "Add mocha" and "Price mocha" are missing from `git log`, and mocha from the files.

## Investigation

The reflog records where `HEAD` was before the reset:

<!-- test: contains=reset: moving to HEAD~3; output -->
```bash
git reflog -3
git log --oneline -1 ORIG_HEAD
```

```text
6833580 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
ecff18a HEAD@{1}: commit: Price mocha
2c389c0 HEAD@{2}: commit: Add mocha
ecff18a Price mocha
```

## Commands

| Command | Shows |
|---|---|
| `git reflog` | every position of HEAD, newest first, with the action |
| `ORIG_HEAD` | HEAD before the last reset / merge / rebase |
| `git log --oneline HEAD@{1}` | the history as it was one move ago |

## Understand the output

`HEAD@{0}: reset: moving to HEAD~3` is the mistake; `HEAD@{1}` (and `ORIG_HEAD`) is the commit "Price mocha", the
branch tip before it. The commits are unreachable, not deleted.

## Root cause

`--hard` with a larger count than intended. `reset` moves the branch; it does not remove commits from the object
store.

## Fix

<!-- test: contains=Price mocha; output -->
```bash
git reset --hard ORIG_HEAD
git log --oneline -3
```

```text
HEAD is now at ecff18a Price mocha
ecff18a (HEAD -> main) Price mocha
2c389c0 Add mocha
269869e Price green tea
```

If other commands ran since (so `ORIG_HEAD` moved), use the reflog entry: `git reset --hard HEAD@{N}`. Uncommitted
changes lost by `--hard` are a different case: Problem 16 and lesson 81.

## Verification

<!-- test: contains=mocha; output -->
```bash
grep mocha menu.txt prices.txt
git status --short | wc -l
```

```text
menu.txt:mocha
prices.txt:mocha 3.90
0
```

## Prevention

- Prefer `git reset --soft` / `--mixed` (keep the changes) and `git revert` for shared commits.
- Before risky commands, mark the spot: `git branch backup-before-cleanup`.
- Know that `git reflog` exists: most "lost" work is recoverable for 30–90 days.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t04
```

Next: [Problem 5 · Deleted branch](problem-05-deleted-branch.md)
