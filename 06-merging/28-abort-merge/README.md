# Lesson 28 · Aborting a merge

> Level 5 · Merging · ⏱ 10 minutes

## What are we learning?

`git merge --abort` returns you to exactly where you were before a merge started. Useful when a conflict is bigger
than expected, or when you merged the wrong branch.

## Visual

```text
 git merge X ──► CONFLICT (half-merged files, markers, MERGE_HEAD)
                    │
                    └── git merge --abort ──► back to the state before the merge: clean, as if nothing happened
```

## Lab setup

<!-- test: contains=lesson-28 -->
```bash
bash scripts/new-lab.sh lesson-28 conflict
cd ~/git-practice/lesson-28
```

## Demonstration

<!-- test: fail; contains=CONFLICT; output -->
```bash
git merge feature-tea 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

While a merge is in progress, Git keeps `MERGE_HEAD` (the commit being merged) and your prompt or `git status` says
"You have unmerged paths". Abort:

<!-- test: contains=nothing to commit, working tree clean; output -->
```bash
ls .git/MERGE_HEAD
git merge --abort
git status
ls .git/MERGE_HEAD 2>&1 || true
```

```text
.git/MERGE_HEAD
On branch main
nothing to commit, working tree clean
ls: cannot access '.git/MERGE_HEAD': No such file or directory
```

Back to the exact state before the merge: same commit, clean working directory, no markers.

## Command breakdown

| Command | What it does |
|---|---|
| `git merge --abort` | cancel an in-progress merge, restore the pre-merge state |
| `git merge --quit` | forget the merge state but keep the files as they are now |
| `git status` | shows whether a merge is in progress |

## Hands-on exercise

**Instructions.** Start the merge again, resolve half of it (edit the file), then change your mind and abort.

**Expected result.** Your half-resolution is discarded; `prices.txt` is `main`'s version again.

<!-- test-run: cd ~/git-practice/lesson-28 && (git merge feature-tea > /dev/null 2>&1 || true) && printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git merge --abort -->

**Verification.**

<!-- test: contains=latte 3.30 -->
```bash
cd ~/git-practice/lesson-28
grep latte prices.txt
```

## Break it

Start a merge with **uncommitted work** in your folder. Git refuses for files the merge would touch; for others it
merges, and then an abort could mix things up. Here: uncommitted work in a file the merge touches.

<!-- test: fail; contains=would be overwritten by merge; output -->
```bash
echo "draft" >> prices.txt
git merge feature-tea 2>&1
```

```text
error: Your local changes to the following files would be overwritten by merge:
	prices.txt
Please commit your changes or stash them before you merge.
Aborting
Merge with strategy ort failed.
```

## Troubleshoot

`Your local changes to the following files would be overwritten by merge`: Git refuses to start, protecting your
uncommitted edit. Nothing was merged; there is nothing to abort. The rule: start merges from a clean working
directory, so that `--abort` can always restore everything.

## Fix

Put the draft aside (lesson 35, `git stash`), merge, abort if needed, bring the draft back:

<!-- test: contains=draft; output -->
```bash
git stash -q
git merge feature-tea > /dev/null 2>&1 || git merge --abort
git stash pop -q
tail -1 prices.txt
```

```text
draft
```

## Real-world example

You start merging `main` into a two-week-old feature branch and get 14 conflicted files. Abort, then make the merge
easier: merge `main` in smaller steps (commit by commit, or one week at a time), or ask the people who changed those
files. `--abort` makes a merge a safe experiment.

## Practice challenge

How can you tell, from the command line only, whether a merge is currently in progress? Write a one-line check.

<details>
<summary>Solution</summary>

<!-- test: contains=merge in progress; output -->
```bash
cd ~/git-practice/lesson-28
git restore prices.txt
git merge feature-tea > /dev/null 2>&1 || true
git rev-parse -q --verify MERGE_HEAD > /dev/null && echo "merge in progress" || echo "no merge"
git merge --abort
```

```text
merge in progress
```

</details>

## Recap

- `git merge --abort` restores the state before the merge started.
- Start merges with a clean working directory (commit or stash first).
- `MERGE_HEAD` exists while a merge is in progress.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-28
```

Next: [Module 07 · Lesson 29 · Undo working directory changes](../../07-undoing/29-restore-working-directory/README.md).
