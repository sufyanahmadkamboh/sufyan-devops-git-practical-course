<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 29 · Undo working directory changes · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

You edited two parts of `prices.txt`. Keep one and discard the other, using `git restore -p`.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-29
git restore --source=HEAD --staged --worktree .
sed -i 's/espresso 2.50/espresso 2.60/; s/cappuccino 3.40/cappuccino 9.99/' prices.txt
printf 's\nn\ny\n' | git restore -p prices.txt > /dev/null
cat prices.txt
```

```text
espresso 2.60
latte 3.20
cappuccino 3.40
```

The two edits are one hunk (lines close together), so `s` splits it; answer `n` (keep) for the espresso change and `y`
(discard) for the cappuccino one.

</details>
