<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 69 · Annotated tags · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Who created `v1.0.0`, and when? Print only the tagger name and date.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-69
git for-each-ref refs/tags/v1.0.0 --format='%(taggername) %(taggerdate:short)'
```

```text
Ada Lovelace 2026-10-05
```

</details>
