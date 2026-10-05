<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 39 · git clone · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Your shallow clone needs the full history after all. Get it without cloning again.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-39/shallow
git fetch -q --unshallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

```text
4
false
```

</details>
