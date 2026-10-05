<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 54 · Merge strategies · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

After a squash merge, delete the PR branch locally the safe way:

```bash
git switch -q main-squash
git branch -d pr-squash 2>&1
```

```text
error: the branch 'pr-squash' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D pr-squash'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
```

## Troubleshoot

`error: the branch 'pr-squash' is not fully merged`: Git checks whether the branch's **commits** are reachable from
the current branch. After a squash they are not (the content is, inside a different commit). Check the content
instead:

```bash
git diff --quiet main-squash pr-squash -- menu.txt prices.txt && echo "identical content: the work is on main-squash"
```

## Fix

Content verified: delete with `-D`. On GitHub, enable "Automatically delete head branches" so merged PR branches are
deleted for you.

```bash
git branch -D pr-squash
```
