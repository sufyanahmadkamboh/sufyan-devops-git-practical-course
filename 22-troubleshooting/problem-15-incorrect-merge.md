# Problem 15 · Incorrect merge

> Troubleshooting lab · run every command from the course folder · related lessons: [23](../06-merging/23-what-is-merge/README.md), [32](../07-undoing/32-git-revert/README.md), [54](../11-pull-requests/54-merge-strategies/README.md)

## Problem

An unfinished branch was merged into `main` and pushed. It must come out of `main`, without rewriting shared history.

<!-- test: contains=lesson-t15 -->
```bash
bash scripts/new-lab.sh lesson-t15 remote
cd ~/git-practice/lesson-t15/ada
git switch -q -c experimental-prices
sed -i 's/espresso 2.50/espresso 9.99/' prices.txt && git commit -q -am "Try premium espresso pricing"
echo "WIP" >> menu.txt && git commit -q -am "WIP menu"
git switch -q main
git merge -q --no-ff --no-edit experimental-prices && git push -q
```

## Symptoms

Production shows the experimental prices and a "WIP" line in the menu.

<!-- test: contains=espresso 9.99; output -->
```bash
head -1 prices.txt
tail -1 menu.txt
```

```text
espresso 9.99
WIP
```

## Investigation

Find the merge and what it brought in:

<!-- test: contains=Merge branch 'experimental-prices'; output -->
```bash
git log --oneline --graph -4
git log --oneline --merges -1
git diff --stat HEAD^1 HEAD
```

```text
*   2fe8abe (HEAD -> main, origin/main, origin/HEAD) Merge branch 'experimental-prices'
|\  
| * 8599e63 (experimental-prices) WIP menu
| * fa09fbb Try premium espresso pricing
|/  
* 4267004 Add prices
2fe8abe (HEAD -> main, origin/main, origin/HEAD) Merge branch 'experimental-prices'
 menu.txt   | 1 +
 prices.txt | 2 +-
 2 files changed, 2 insertions(+), 1 deletion(-)
```

## Commands

| Command | Shows |
|---|---|
| `git log --merges` | merge commits |
| `git show MERGE` / `git log -1 --format=%P MERGE` | the merge and its parents (1st = main before, 2nd = merged branch) |
| `git diff MERGE^1 MERGE` | everything the merge brought into main |

## Understand the output

The merge commit's first parent is `main` before the mistake; its second parent is the experimental branch. `HEAD^1
→ HEAD` shows the full effect of the merge: two files changed. Others may have pulled `main` already, so resetting it
is not an option.

## Root cause

The wrong branch was merged (or merged too early). A PR review or protected `main` would have stopped it.

## Fix

Revert the merge, keeping the first parent (`main`'s side), as a new commit:

<!-- test: contains=Revert "Merge branch 'experimental-prices'"; output -->
```bash
git revert -m 1 --no-edit HEAD 2>&1 | head -1
git push -q
git log --oneline -2
```

```text
[main 177a2d1] Revert "Merge branch 'experimental-prices'"
177a2d1 (HEAD -> main, origin/main, origin/HEAD) Revert "Merge branch 'experimental-prices'"
2fe8abe Merge branch 'experimental-prices'
```

Important for later: `main` now "knows" the branch's commits but not their changes. When the branch is ready and
merged again, Git only brings what changed **after** the revert. To bring everything, first revert the revert
(`git revert <revert-commit>`), then merge.

## Verification

<!-- test: contains=espresso 2.50; absent=WIP; output -->
```bash
head -1 prices.txt
tail -1 menu.txt
git status | head -2
```

```text
espresso 2.50
cappuccino
On branch main
Your branch is up to date with 'origin/main'.
```

## Prevention

- Merge only through reviewed PRs into a protected `main` (lessons 52–59).
- Name unfinished work clearly (`wip/…`, draft PRs) and keep it out of the merge queue.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t15
```

Next: [Problem 16 · Lost commit](problem-16-lost-commit.md)
