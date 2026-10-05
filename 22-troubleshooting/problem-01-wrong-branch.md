# Problem 1 · Committed on the wrong branch

> Troubleshooting lab · run every command from the course folder · related lessons: [17](../05-branches/17-why-branches/README.md), [21](../05-branches/21-branch-visualization/README.md), [31](../07-undoing/31-git-reset/README.md)

## Problem

You meant to start a feature branch, but committed two commits directly on `main`.

<!-- test: contains=lesson-t01 -->
```bash
bash scripts/new-lab.sh lesson-t01 basic
cd ~/git-practice/lesson-t01
echo "chai" >> menu.txt && git commit -q -am "Add chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
```

## Symptoms

The feature's commits appear on `main`; the branch you wanted does not exist.

<!-- test: contains=main; output -->
```bash
git branch
git log --oneline -3
```

```text
* main
0829a32 (HEAD -> main) Price chai
5b8dbad Add chai
4267004 Add prices
```

## Investigation

Which branch am I on, and which commits are not supposed to be on it? Compare with the last known-good point (here
the shared `main` ends at "Add prices"; with a remote, `origin/main`):

<!-- test: contains=Price chai; output -->
```bash
git branch --show-current
git log --oneline 4267004..main
git status --short | wc -l
```

```text
main
0829a32 (HEAD -> main) Price chai
5b8dbad Add chai
0
```

## Commands

| Command | Shows |
|---|---|
| `git branch --show-current` | the current branch |
| `git log --oneline origin/main..main` | local commits not on the server |
| `git status` | uncommitted work (must be clean or stashed before moving things) |

## Understand the output

Two commits after `4267004` are on `main`; the working directory is clean (0 changes). Nothing is pushed (or `git
status` would say "ahead of 'origin/main' by 2 commits" before a push and "up to date" after).

## Root cause

`git switch -c feature` was forgotten before committing. Commits always go to the branch `HEAD` points to.

## Fix

Create the branch where `main` is now (it keeps the commits), then move `main` back:

<!-- test: contains=Price chai; output -->
```bash
git branch feature-chai
git reset -q --hard 4267004
git switch -q feature-chai
git log --oneline -3
```

```text
0829a32 (HEAD -> feature-chai) Price chai
5b8dbad Add chai
4267004 (main) Add prices
```

If the commits were **already pushed** to a shared `main`, do not reset it: leave them, or revert them (Problem 18).

## Verification

<!-- test: contains=feature-chai; output -->
```bash
git log --oneline -1 main
git log --oneline main..feature-chai
git branch --show-current
```

```text
4267004 (main) Add prices
0829a32 (HEAD -> feature-chai) Price chai
5b8dbad Add chai
feature-chai
```

## Prevention

- A shell prompt that shows the branch (Git's `git-prompt.sh`, starship, oh-my-zsh).
- Protect `main` on the server so direct pushes fail (lesson 59).
- Start every task with `git switch -c NAME`.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t01
```

Next: [Problem 2 · Merge conflict](problem-02-merge-conflict.md)
