<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 87 · Git worktrees · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Try to check out `main` in the main worktree as well:

```bash
git switch main 2>&1
```

```text
fatal: 'main' is already used by worktree at '~/git-practice/lesson-87-hotfix'
```

## Troubleshoot

`fatal: 'main' is already used by worktree at '…/lesson-87-hotfix'`: two folders on the same branch would each
move it independently. Git allows each branch in one worktree only.

## Fix

Finish with the hotfix worktree and remove it; then `main` is free:

```bash
git stash -q
git worktree remove ../lesson-87-hotfix
git worktree list
git switch -q main && git branch --show-current
git switch -q feature-tea && git stash pop -q
```

```text
~/git-practice/lesson-87 bb67674 [feature-tea]
main
```
