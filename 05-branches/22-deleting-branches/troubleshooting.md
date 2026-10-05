<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 22 · Deleting branches · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

```bash
git branch -d experiment 2>&1
```

```text
error: the branch 'experiment' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D experiment'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
```

## Troubleshoot

`error: the branch 'experiment' is not fully merged`: `experiment` has a commit (`Try oat milk`) that no other branch
contains; deleting the label would leave that commit unreachable. Look at what would be lost:

```bash
git log --oneline main..experiment
```

## Fix

Decide. Either merge the work first, or confirm it is really unwanted and force the delete. Here the experiment is
abandoned, so force it, and note the commit ID first (lesson 79 shows how to get it back anyway):

```bash
git rev-parse --short experiment
git branch -D experiment
```

```text
6bc77c1
Deleted branch experiment (was 6bc77c1).
```
