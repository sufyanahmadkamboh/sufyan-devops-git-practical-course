<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 87 · Git worktrees · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Delete a worktree folder with `rm -rf` (as people often do), then clean up Git's records.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-87
git worktree add -q --detach ../lesson-87-review main
rm -rf ../lesson-87-review
git worktree prune
git worktree list
```

```text
~/git-practice/lesson-87 bb67674 [feature-tea]
```

</details>
