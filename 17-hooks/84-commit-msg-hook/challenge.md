<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 84 · Commit message hook · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

List the commits since `4267004` grouped by type, as a changelog generator would.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-84
git log --format=%s 4267004..HEAD | sed -E 's/^([a-z]+).*/\1/' | sort | uniq -c
```

```text
      2 feat
      1 fix
```

</details>
