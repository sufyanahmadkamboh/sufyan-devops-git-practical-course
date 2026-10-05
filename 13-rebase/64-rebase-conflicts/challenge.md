<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 64 · Rebase conflicts · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Enable `rerere`, resolve the conflict once, then abort the rebase, start it again, and watch Git resolve it for you.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-64
git config rerere.enabled true
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
git rebase main 2>&1 | grep -i "resolved" || true
git rebase --abort
```

```text
Recorded resolution for 'prices.txt'.
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
hint: Resolve all conflicts manually, mark them as resolved with
Resolved 'prices.txt' using previous resolution.
```

</details>
