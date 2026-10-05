<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 36 · Managing stashes · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Write a one-liner that prints, for every stash, its name and the number of files it changes.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-36
git stash push -q -m "recipe again"
git stash list --format=%gd | while read -r s; do echo "$s $(git stash show --name-only "$s" | wc -l) file(s)"; done
```

```text
stash@{0} 1 file(s)
```

</details>
