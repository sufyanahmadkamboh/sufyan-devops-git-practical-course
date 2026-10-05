<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 51 · What is a pull request? · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

How many commits ahead of and behind `main` is `feature-tea` in the first lab (GitHub shows this as "N commits ahead,
M commits behind main")?

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-51
git rev-list --left-right --count main...feature-tea | awk '{print "behind", $1, "ahead", $2}'
```

```text
behind 1 ahead 1
```

</details>
