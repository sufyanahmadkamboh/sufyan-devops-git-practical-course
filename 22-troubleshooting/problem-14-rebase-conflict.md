# Problem 14 · Rebase conflict

> Troubleshooting lab · run every command from the course folder · related lessons: [64](../13-rebase/64-rebase-conflicts/README.md), [65](../13-rebase/65-abort-rebase/README.md), [66](../13-rebase/66-continue-rebase/README.md)

## Problem

`git pull --rebase` (or `git rebase main`) stops halfway; the prompt says `REBASE 1/2` and nothing seems to work.

<!-- test: contains=lesson-t14 -->
```bash
bash scripts/new-lab.sh lesson-t14 conflict
cd ~/git-practice/lesson-t14
git switch -q feature-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
```

<!-- test: fail; contains=CONFLICT; output -->
```bash
git rebase main 2>&1 | grep -E "CONFLICT|could not apply"
test "${PIPESTATUS[0]}" -eq 0
```

```text
CONFLICT (content): Merge conflict in prices.txt
error: could not apply 00931cc... Raise the latte price to 3.50
```

## Symptoms

`git status` reports a rebase in progress; `git commit`, `git switch` and `git pull` refuse or behave unexpectedly.

<!-- test: fail; contains=while rebasing; output -->
```bash
git switch main 2>&1
```

```text
fatal: cannot switch branch while rebasing
Consider "git rebase --quit" or "git worktree add".
```

## Investigation

<!-- test: contains=rebase in progress; output -->
```bash
git status
```

```text
interactive rebase in progress; onto 594657b
Last command done (1 command done):
   pick 00931cc # Raise the latte price to 3.50
Next command to do (1 remaining command):
   pick d859121 # Add green tea
  (use "git rebase --edit-todo" to view and edit)
You are currently rebasing branch 'feature-tea' on '594657b'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

## Commands

| Command | Shows |
|---|---|
| `git status` | the commit being replayed, the remaining ones, the conflicted files |
| `git diff` | the conflict in the file |
| `git log --oneline -1 REBASE_HEAD` | the commit Git is trying to apply |
| `git rebase --show-current-patch` | that commit's full change |

## Understand the output

"rebase in progress; onto 594657b" and "Last command done: pick 00931cc Raise the latte price to 3.50": Git replayed
nothing yet successfully; the first of your two commits conflicts with `main` (both changed the latte line). "Next
command to do: pick … Add green tea" is still waiting. Note the reversed sides: `HEAD` (ours) is `main`, the incoming
side (theirs) is **your** commit.

## Root cause

Your branch and `main` changed the same line; rebase applies your commits one by one, so the conflict appears at the
commit that touched it.

## Fix

Resolve **this** commit, mark it, continue; repeat if another commit conflicts:

<!-- test: contains=Successfully rebased; output -->
```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git rebase --continue 2>&1 | tail -1
```

```text
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
```

Too tangled? `git rebase --abort` returns everything to the state before the rebase.

## Verification

<!-- test: contains=Add green tea; output -->
```bash
git log --oneline --graph -4
git status | head -2
```

```text
* 5161eb4 (HEAD -> feature-tea) Add green tea
* f39bf7d Raise the latte price to 3.50
* 594657b (main) Raise the latte price to 3.30
* 4267004 Add prices
On branch feature-tea
nothing to commit, working tree clean
```

## Prevention

- Rebase often (small steps) rather than once after weeks.
- `git config --global rerere.enabled true` to reuse resolutions; `merge.conflictStyle zdiff3` for context.
- Prefer merging `main` into long-lived shared branches instead of rebasing them.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t14
```

Next: [Problem 15 · Incorrect merge](problem-15-incorrect-merge.md)
