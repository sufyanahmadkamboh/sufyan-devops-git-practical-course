<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 75 · Git objects · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Read `prices.txt` as it was in the first commit that had it, without checking anything out.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-75
git cat-file -p 4267004:prices.txt
```

```text
espresso 2.50
latte 3.20
cappuccino 3.40
```

</details>
