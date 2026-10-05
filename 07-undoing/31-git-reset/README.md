# Lesson 31 · git reset: soft, mixed and hard

> Level 6 · Undoing changes · ⏱ 25 minutes

## What are we learning?

`git reset COMMIT` moves the current branch back to an earlier commit. Its three modes decide what happens to the
work of the commits you step back over: keep it staged, keep it unstaged, or delete it.

## Visual

```text
 before:   A ── B ── C  ← main (HEAD)        git reset ... B

                     moves the branch     staging area      working directory
 --soft     B        yes                  keeps C's work    keeps C's work     → "uncommit", ready to recommit
 --mixed    B        yes                  reset to B        keeps C's work     → "uncommit and unstage" (default)
 --hard     B        yes                  reset to B        reset to B         → C's work is GONE from your folder

 after:    A ── B  ← main (HEAD)     C still exists, unreferenced: reflog can find it (lesson 33)
```

## Lab setup

<!-- test: contains=lesson-31 -->
```bash
bash scripts/new-lab.sh lesson-31 history
cd ~/git-practice/lesson-31
git log --oneline
```

## Demonstration

**--soft**: undo the last commit, keep its changes staged:

<!-- test: contains=M  prices.txt; output -->
```bash
git reset --soft HEAD~1
git log --oneline -1
git status --short
```

```text
2c389c0 (HEAD -> main) Add mocha
M  prices.txt
```

The commit "Price mocha" is gone from the branch; its change is staged, ready to be committed again (with a better
message, for example):

<!-- test: contains=Add the mocha price -->
```bash
git commit -q -m "Add the mocha price"
git log --oneline -1
```

**--mixed** (the default): undo the last commit and unstage:

<!-- test: contains= M prices.txt; output -->
```bash
git reset HEAD~1
git status --short
```

```text
Unstaged changes after reset:
M	prices.txt
 M prices.txt
```

**--hard**: undo and throw the changes away:

<!-- test: contains=nothing to commit; output -->
```bash
git reset --hard HEAD~1
git log --oneline -1
git status
```

```text
HEAD is now at 269869e Price green tea
269869e (HEAD -> main) Price green tea
On branch main
nothing to commit, working tree clean
```

`--hard` removed both the "Add mocha" commit and the uncommitted mocha price from your folder.

## Command breakdown

| Command | Branch | Staging area | Working directory |
|---|---|---|---|
| `git reset --soft C` | → C | unchanged | unchanged |
| `git reset C` (`--mixed`) | → C | = C | unchanged |
| `git reset --hard C` | → C | = C | = C (uncommitted work lost!) |
| `git reset FILE` | — | FILE = HEAD | unchanged (= `restore --staged`) |

`HEAD~1` is one commit back, `HEAD~3` three; `ORIG_HEAD` is where the branch was before the last reset.

## Hands-on exercise

**Instructions.** Squash the last two commits ("Add green tea", "Price green tea") into one using `--soft`.

**Expected result.** One commit "Add green tea with its price" containing both changes.

<!-- test-run: cd ~/git-practice/lesson-31 && git reset -q --soft HEAD~2 && git commit -q -m "Add green tea with its price" -->

**Verification.**

<!-- test: contains=Add green tea with its price; contains=2 files changed -->
```bash
cd ~/git-practice/lesson-31
git show --stat --format=%s HEAD
```

## Break it

The classic mistake: `--hard` with uncommitted work you wanted to keep.

<!-- test: absent=flat white -->
```bash
echo "flat white 3.60" >> prices.txt
git reset --hard HEAD~1
cat prices.txt
```

## Troubleshoot

Two different things were lost:

1. **The commit** "Add green tea with its price": recoverable, it still exists as an object; the reflog knows it.
2. **The uncommitted line** "flat white 3.60": never committed or staged, so it is gone for good.

<!-- test: contains=reset: moving to HEAD~1; output -->
```bash
git reflog -3
```

```text
4267004 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1
6ba9a63 HEAD@{1}: commit: Add green tea with its price
4267004 (HEAD -> main) HEAD@{2}: reset: moving to HEAD~2
```

## Fix

Bring the commit back: `ORIG_HEAD` (or the reflog entry `HEAD@{1}`) is where `main` was before the reset:

<!-- test: contains=Add green tea with its price; output -->
```bash
git reset --hard ORIG_HEAD
git log --oneline -2
```

```text
HEAD is now at 6ba9a63 Add green tea with its price
6ba9a63 (HEAD -> main) Add green tea with its price
4267004 Add prices
```

The commit is back; the uncommitted line is not. Lesson 33 and lesson 81 go deeper into recovering after a hard reset.

## Real-world example

`reset` rewrites the branch: do it only on commits that have **not been pushed** (or only on your own feature branch,
followed by a `--force-with-lease` push, lesson 42). For a commit already on a shared `main`, use `git revert`
(lesson 32), which undoes it with a new commit instead of removing history.

## Practice challenge

Without `--hard`, remove the last commit **and** keep its changes only in your working directory (not staged). Which
mode is that? Then show what the removed commit had changed.

<details>
<summary>Solution</summary>

<!-- test: contains= M; output -->
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

## Recap

- `reset` moves the branch; `--soft` keeps changes staged, `--mixed` unstaged, `--hard` deletes them.
- Commits removed by reset are recoverable (reflog, `ORIG_HEAD`); uncommitted work removed by `--hard` is not.
- Never reset commits others already have: use `revert`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-31
```

Next: [Lesson 32 · git revert](../32-git-revert/README.md).
