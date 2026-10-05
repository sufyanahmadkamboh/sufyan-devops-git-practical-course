<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 71 · Git blame · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Show only the authors' names and how many lines of `prices.txt` each last changed, ignoring the reformatting.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-71
git blame --line-porcelain prices.txt | sed -n 's/^author //p' | sort | uniq -c
```

```text
      2 Ada Lovelace
      1 Grace Hopper
```

</details>
