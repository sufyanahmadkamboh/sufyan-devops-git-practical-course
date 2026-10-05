<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 85 · Git hooks in teams · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show the path of the `commit-msg` hook Git uses in Grace's clone now.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-85/grace
git rev-parse --git-path hooks/commit-msg
```

```text
.githooks/commit-msg
```

`--git-path` resolves paths inside the repository's Git directory, honouring `core.hooksPath`.

</details>
