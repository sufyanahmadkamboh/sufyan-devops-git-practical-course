# Problem 11 · Wrong upstream branch

> Troubleshooting lab · run every command from the course folder · related lessons: [43](../09-remotes/43-upstream-branches/README.md), [42](../09-remotes/42-git-push/README.md)

## Problem

You created a fix branch from `origin/main`. `git status` compares it with `main`, `git pull` pulls `main`, and `git
push` refuses.

<!-- test: contains=lesson-t11 -->
```bash
bash scripts/new-lab.sh lesson-t11 remote
cd ~/git-practice/lesson-t11/ada
git switch -q -c fix-latte origin/main
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price"
```

## Symptoms

<!-- test: fail; contains=upstream branch of your current branch does not match; output -->
```bash
git status | head -2
git push 2>&1
```

```text
On branch fix-latte
Your branch is ahead of 'origin/main' by 1 commit.
fatal: The upstream branch of your current branch does not match
the name of your current branch.  To push to the upstream branch
on the remote, use

    git push origin HEAD:main

To push to the branch of the same name on the remote, use

    git push origin HEAD

To choose either option permanently, see push.default in 'git help config'.

To avoid automatically configuring an upstream branch when its name
won't match the local branch, see option 'simple' of branch.autoSetupMerge
in 'git help config'.
```

## Investigation

<!-- test: contains=[origin/main: ahead 1]; output -->
```bash
git branch -vv
git rev-parse --abbrev-ref '@{upstream}'
```

```text
* fix-latte 8a517e0 [origin/main: ahead 1] Fix the latte price
  main      4267004 [origin/main] Add prices
origin/main
```

## Commands

| Command | Shows |
|---|---|
| `git branch -vv` | every branch's upstream in `[…]` with ahead/behind |
| `git rev-parse --abbrev-ref @{u}` | the current branch's upstream |
| `git config push.default` | how a plain `git push` chooses the target (`simple` by default) |

## Understand the output

`fix-latte` tracks `origin/main` (`git switch -c NAME origin/main` sets that up automatically). With the default
`push.default=simple`, Git refuses to push a branch to an upstream with a different name, which is what saved you
from pushing the fix directly into `main`.

## Root cause

The branch was created from a remote-tracking branch, so it inherited it as upstream.

## Fix

Push the branch under its own name and make that the upstream:

<!-- test: contains=origin/fix-latte; output -->
```bash
git push -q -u origin fix-latte 2>&1
git branch -vv | grep fix-latte
```

```text
* fix-latte 8a517e0 [origin/fix-latte] Fix the latte price
```

(Or: `git branch --unset-upstream` / `git branch -u origin/fix-latte` once the remote branch exists.)

## Verification

<!-- test: contains=up to date with 'origin/fix-latte'; output -->
```bash
git status | head -2
```

```text
On branch fix-latte
Your branch is up to date with 'origin/fix-latte'.
```

## Prevention

- Create branches from the local `main` (`git switch main && git pull && git switch -c NAME`), or use
  `git switch -c NAME --no-track origin/main`.
- `git config --global push.autoSetupRemote true`: the first `git push` creates and tracks `origin/NAME`.
- Keep `push.default=simple` (the default).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t11
```

Next: [Problem 12 · Accidentally committed secret](problem-12-committed-secret.md)
