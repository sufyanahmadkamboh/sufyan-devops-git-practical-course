<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 65 · Aborting a rebase · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Finish a rebase, then decide you want the old branch back anyway. Undo it **after** it completed.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-65
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
grep latte prices.txt
```

```text
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
latte 3.50
```

After a completed rebase, `ORIG_HEAD` (or `git reflog`, the line before `rebase (start)`) is the old tip.

</details>
