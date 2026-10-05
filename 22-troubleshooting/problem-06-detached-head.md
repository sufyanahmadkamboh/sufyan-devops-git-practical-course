# Problem 6 · Detached HEAD

> Troubleshooting lab · run every command from the course folder · related lessons: [76](../15-git-internals/76-head/README.md), [78](../15-git-internals/78-detached-head/README.md)

## Problem

You checked out a release tag to look at it, fixed something, committed, and switched back. The fix is nowhere.

<!-- test: contains=lesson-t06 -->
```bash
bash scripts/new-lab.sh lesson-t06 history
cd ~/git-practice/lesson-t06
git tag v1.0.0 4267004
git checkout -q v1.0.0
sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix the espresso price"
git switch -q main 2> /dev/null
```

## Symptoms

<!-- test: contains=espresso 2.50; output -->
```bash
git log --oneline --all | grep -c Hotfix || true
grep espresso prices.txt
```

```text
0
espresso 2.50
```

`git log --all` does not show the commit; `main` still has the old price.

## Investigation

Was HEAD detached when committing? The reflog shows the checkout of a commit ID (not a branch) and the commit made
there:

<!-- test: contains=checkout: moving from main to v1.0.0; output -->
```bash
git reflog -3
```

```text
ecff18a (HEAD -> main) HEAD@{0}: checkout: moving from fdfffaaf7d8dfe545da91709157378fd1d26884c to main
fdfffaa HEAD@{1}: commit: Hotfix the espresso price
4267004 (tag: v1.0.0) HEAD@{2}: checkout: moving from main to v1.0.0
```

## Commands

| Command | Shows |
|---|---|
| `git status` | "HEAD detached at …" while detached |
| `git reflog` | `checkout: moving from main to v1.0.0`, then commits made there |
| `git branch --contains SHA` | which branches contain a commit (none for a lost one) |

## Understand the output

`checkout: moving from main to v1.0.0` detached HEAD at the tag; `commit: Hotfix the espresso price` was made
there; then `checkout: moving from … to main` left it behind. No branch was ever moved to the hotfix.

## Root cause

Commits made in detached HEAD belong to no branch; switching away leaves them unreferenced (Git printed a warning
with the commit ID).

## Fix

Give it a branch, then bring it where it belongs:

<!-- test: contains=espresso 2.45; output -->
```bash
fix=$(git reflog --format=%h --grep-reflog="commit: Hotfix" | head -1)
git branch hotfix-espresso "$fix"
git cherry-pick hotfix-espresso > /dev/null
grep espresso prices.txt
```

```text
espresso 2.45
```

## Verification

<!-- test: contains=main; output -->
```bash
git branch --contains "$(git log --format=%h -1 --grep=Hotfix main)"
git status | head -1
```

```text
* main
On branch main
```

## Prevention

- When Git says "You are in 'detached HEAD' state", create a branch before committing: `git switch -c NAME`.
- Inspect old versions with `git switch --detach TAG` consciously, or use a worktree (lesson 87).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t06
```

Next: [Problem 7 · Wrong remote](problem-07-wrong-remote.md)
