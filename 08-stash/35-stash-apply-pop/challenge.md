<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 35 · Stash, apply and pop · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Stash a change that is partly staged and partly unstaged, then restore it with exactly the same staged/unstaged split.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-35
git stash -q
echo "mocha" >> menu.txt && git add menu.txt
sed -i 's/latte 3.40/latte 3.50/' prices.txt
git stash -q
git stash pop -q --index
git status --short
```

```text
M  menu.txt
 M prices.txt
```

Without `--index`, everything comes back unstaged.

</details>
