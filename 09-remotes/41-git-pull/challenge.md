<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 41 · git pull · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Set up Ada's clone so that `git pull` always rebases and automatically stashes uncommitted changes before doing so.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-41/ada
git config pull.rebase true
git config rebase.autoStash true
git config --get pull.rebase && git config --get rebase.autoStash
```

```text
true
true
```

</details>
