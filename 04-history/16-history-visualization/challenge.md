<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 16 · Commit history visualization · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

How many commits does `main` have that `feature-tea` does not, and the other way round? Answer with one command.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-16
git rev-list --left-right --count main...feature-tea
```

```text
2	0
```

Left number: commits only on `main` (the opening hours and the merge); right: only on `feature-tea` (0: it has been
merged, so everything it has is on `main` too).

</details>
