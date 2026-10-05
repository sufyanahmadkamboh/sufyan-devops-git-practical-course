<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 38 · git remote · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Remove the `original` remote and prove its remote-tracking branches are gone too.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-38/ada
git remote remove original
git remote
git branch -r
```

```text
origin
  origin/HEAD -> origin/main
  origin/main
```

</details>
