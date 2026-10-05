# Problem 5 · Deleted branch

> Troubleshooting lab · run every command from the course folder · related lessons: [22](../05-branches/22-deleting-branches/README.md), [79](../16-recovery/79-recover-deleted-branch/README.md)

## Problem

Cleaning up branches, you force-deleted one that was not merged yet.

<!-- test: contains=lesson-t05 -->
```bash
bash scripts/new-lab.sh lesson-t05 basic
cd ~/git-practice/lesson-t05
git switch -q -c seasonal-menu
echo "pumpkin latte" >> menu.txt && git commit -q -am "Add pumpkin latte"
echo "pumpkin latte 4.20" >> prices.txt && git commit -q -am "Price pumpkin latte"
git switch -q main
```

<!-- test: contains=Deleted branch seasonal-menu; output -->
```bash
git branch -D seasonal-menu
```

```text
Deleted branch seasonal-menu (was b4d90ba).
```

## Symptoms

`git branch` no longer lists it; `git switch seasonal-menu` fails; the work is not on `main`.

<!-- test: fail; contains=invalid reference; output -->
```bash
git switch seasonal-menu 2>&1
```

```text
fatal: invalid reference: seasonal-menu
```

## Investigation

The deletion message printed the tip (`was …`). If it scrolled away, the reflog has the branch's last commit:

<!-- test: contains=Price pumpkin latte; output -->
```bash
git reflog | grep -m2 "pumpkin"
```

```text
b4d90ba HEAD@{1}: commit: Price pumpkin latte
129db21 HEAD@{2}: commit: Add pumpkin latte
```

## Commands

| Command | Shows |
|---|---|
| `git reflog` | commits HEAD was on, including the deleted branch's |
| `git log -g --grep-reflog=TEXT` | search the reflog |
| `git fsck --unreachable --no-reflogs` | commits nothing refers to (if you never had the branch checked out) |

## Understand the output

`commit: Price pumpkin latte` is the newest commit made on the branch: its tip. Its parent chain contains the rest of
the branch's commits.

## Root cause

`git branch -D` deletes even unmerged branches (`-d` would have refused). A branch is a pointer; the commits remain.

## Fix

<!-- test: contains=Price pumpkin latte; output -->
```bash
tip=$(git reflog --format=%h --grep-reflog="commit: Price pumpkin latte" | head -1)
git branch seasonal-menu "$tip"
git log --oneline main..seasonal-menu
```

```text
b4d90ba (seasonal-menu) Price pumpkin latte
129db21 Add pumpkin latte
```

## Verification

<!-- test: contains=pumpkin latte 4.20 -->
```bash
git show seasonal-menu:prices.txt | tail -1
```

## Prevention

- Delete with `git branch -d` (refuses unmerged branches); use `-D` only after checking.
- Push work-in-progress branches: the server and teammates keep a copy.
- Protect important branches from deletion on the server.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t05
```

Next: [Problem 6 · Detached HEAD](problem-06-detached-head.md)
