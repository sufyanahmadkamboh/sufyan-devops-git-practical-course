<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 31 · git reset: soft, mixed and hard · challenge

> The full lesson: [README.md](README.md)

## Practice challenge

Without `--hard`, remove the last commit **and** keep its changes only in your working directory (not staged). Which
mode is that? Then show what the removed commit had changed.

<details>
<summary>Solution</summary>

```bash
cd ~/git-practice/lesson-31
git reset --mixed HEAD~1
git status --short
git diff --stat
git reset -q --hard ORIG_HEAD
```

```text
Unstaged changes after reset:
M	menu.txt
M	prices.txt
 M menu.txt
 M prices.txt
 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
```

`--mixed` (the default). The last line puts everything back for the next learner step.

</details>
