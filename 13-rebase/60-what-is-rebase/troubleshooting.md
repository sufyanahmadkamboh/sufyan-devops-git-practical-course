<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 60 · What is rebase? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Rebase a branch that was **already pushed**, then push it:

```bash
git init -q --bare ../lesson-60-server.git && git remote add origin ../lesson-60-server.git
git push -q -u origin main feature-tea
git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Raise the espresso price" && git push -q
git switch -q feature-tea && git rebase -q main
git push 2>&1
```

```text
To ../lesson-60-server.git
 ! [rejected]        feature-tea -> feature-tea (non-fast-forward)
error: failed to push some refs to '../lesson-60-server.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

The server has the old `feature-tea` (with the old commit); your rebased branch does not contain it, so the push is
not a fast-forward and is rejected. Rebase **rewrote history** that someone else might already have.

The golden rule: **never rebase commits that others have built on.** Your own unshared commits, or your own feature
branch that only you use, are fine.

## Fix

It is Ada's own feature branch, nobody else works on it: replace it, safely.

```bash
git push --force-with-lease 2>&1
```

```text
To ../lesson-60-server.git
 + a60fd19...af882cf feature-tea -> feature-tea (forced update)
```
