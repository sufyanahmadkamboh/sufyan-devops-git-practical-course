<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 14 · git show · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show only the names of the files changed by the last three commits together, each name once.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-14
git diff --name-only HEAD~3 HEAD
```

```text
menu.txt
prices.txt
```

Comparing the snapshot from three commits ago with the latest gives the combined list (`git show` shows commits one
at a time).

</details>
