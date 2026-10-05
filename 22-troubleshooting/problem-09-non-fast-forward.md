# Problem 9 · Non-fast-forward error

> Troubleshooting lab · run every command from the course folder · related lessons: [42](../09-remotes/42-git-push/README.md), [60](../13-rebase/60-what-is-rebase/README.md), [63](../13-rebase/63-interactive-rebase/README.md)

## Problem

You cleaned up your already-pushed feature branch (amended the last commit) and now cannot push it.

<!-- test: contains=lesson-t09 -->
```bash
bash scripts/new-lab.sh lesson-t09 remote
cd ~/git-practice/lesson-t09/ada
git switch -q -c feature-chai
echo "chai" >> menu.txt && git commit -q -am "Add chia"
git push -q -u origin feature-chai
git commit -q --amend -m "Add chai"
```

## Symptoms

<!-- test: fail; contains=non-fast-forward; output -->
```bash
git push 2>&1
```

```text
To ~/git-practice/lesson-t09/server/cafe.git
 ! [rejected]        feature-chai -> feature-chai (non-fast-forward)
error: failed to push some refs to '~/git-practice/lesson-t09/server/cafe.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Investigation

Compare your branch with its pushed version:

<!-- test: contains=have diverged; output -->
```bash
git status | head -3
git log --oneline --graph feature-chai origin/feature-chai | head -4
```

```text
On branch feature-chai
Your branch and 'origin/feature-chai' have diverged,
and have 1 and 1 different commits each, respectively.
* 4c5181d (HEAD -> feature-chai) Add chai
| * 37189fb (origin/feature-chai) Add chia
|/  
* 4267004 (origin/main, origin/HEAD, main) Add prices
```

## Commands

| Command | Shows |
|---|---|
| `git status` | "Your branch and 'origin/…' have diverged" |
| `git log --graph BRANCH origin/BRANCH` | the two versions side by side |
| `git reflog` | the commit before the amend/rebase |

## Understand the output

`! [rejected] … (non-fast-forward)` / "Updates were rejected because the tip of your current branch is behind its
remote counterpart". Here "behind" is misleading: the branches **diverged** because `--amend` replaced "Add chia"
with a new commit "Add chai". The server's version is not contained in yours.

## Root cause

History was rewritten (amend, rebase, reset) after pushing.

## Fix

Decide whose branch it is:

- **Only you use it** (a feature branch before review): replace the remote version, safely.
- **Others have pulled it**: do not rewrite; restore the pushed version and add a new commit instead.

It is Ada's own branch:

<!-- test: contains=forced update; output -->
```bash
git push --force-with-lease 2>&1
```

```text
To ~/git-practice/lesson-t09/server/cafe.git
 + 37189fb...4c5181d feature-chai -> feature-chai (forced update)
```

`--force-with-lease` refuses if someone else pushed to the branch since your last fetch; `--force` would not check.

## Verification

<!-- test: contains=up to date; output -->
```bash
git status | head -2
git log --oneline -1 origin/feature-chai
```

```text
On branch feature-chai
Your branch is up to date with 'origin/feature-chai'.
4c5181d (HEAD -> feature-chai, origin/feature-chai) Add chai
```

## Prevention

- Rewrite history only before pushing, or only on branches nobody else uses.
- Use `--force-with-lease`, never plain `--force`; protect `main` against force pushes (lesson 59).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t09
```

Next: [Problem 10 · Authentication failure](problem-10-authentication-failure.md)
