<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 32 · git revert · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Undo the last two commits with a **single** revert commit.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-32
git revert --no-commit HEAD~1..HEAD
git commit -q -m "Revert the last two commits"
git log --oneline -1
```

```text
05608e7 (HEAD -> main) Revert the last two commits
```

</details>
