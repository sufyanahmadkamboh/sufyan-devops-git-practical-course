# Lesson 60 · What is rebase?

> Level 13 · Rebase · ⏱ 20 minutes

## What are we learning?

Rebase **replays** your branch's commits on top of another commit, as if you had started your work later. The result
is a straight history, but the replayed commits are **new commits** with new IDs. Understanding that one fact explains
every rule about rebase.

## Visual

```text
 before:                                     git rebase main (on feature-tea)

 A ── B ── D            ← main               A ── B ── D            ← main
       ╲                                                 ╲
        C               ← feature-tea                     C'        ← feature-tea

 C' has the same change and message as C, but a different parent (D instead of B),
 so a different ID. C still exists (reflog), but nothing points to it any more.
```

How Git does it, step by step:

```text
 1. find the commits on feature-tea that are not on main        → C
 2. move feature-tea to main's tip                               → D
 3. re-apply each of those commits, in order, as new commits     → C'
```

## Lab setup

<!-- test: contains=lesson-60 -->
```bash
bash scripts/new-lab.sh lesson-60 diverged
cd ~/git-practice/lesson-60
git log --oneline --graph --all
```

## Demonstration

Remember the branch's commit ID, then rebase:

<!-- test: contains=Successfully rebased; output -->
```bash
before=$(git rev-parse --short feature-tea)
git switch -q feature-tea
git rebase main
echo "feature-tea was $before, is now $(git rev-parse --short HEAD)"
```

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/feature-tea.
feature-tea was bb67674, is now a60fd19
```

<!-- test: output -->
```bash
git log --oneline --graph --all
```

```text
* a60fd19 (HEAD -> feature-tea) Add green tea to the menu
* f40d080 (main) Add opening hours
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

A straight line: "Add green tea" now comes after "Add opening hours". Same message, same change, new ID. The old
commit is still in the reflog:

<!-- test: contains=rebase (start); output -->
```bash
git reflog -4
```

```text
a60fd19 (HEAD -> feature-tea) HEAD@{0}: rebase (finish): returning to refs/heads/feature-tea
a60fd19 (HEAD -> feature-tea) HEAD@{1}: rebase (pick): Add green tea to the menu
f40d080 (main) HEAD@{2}: rebase (start): checkout main
bb67674 HEAD@{3}: checkout: moving from main to feature-tea
```

## Command breakdown

| Command | What it does |
|---|---|
| `git rebase BASE` | replay the current branch's own commits on top of BASE |
| `git rebase BASE BRANCH` | switch to BRANCH first, then rebase it |
| `git rebase -i BASE` | interactive: choose what happens to each commit (lesson 63) |
| `git pull --rebase` | fetch + rebase your local commits on the remote branch |

## Hands-on exercise

**Instructions.** Prove that the rebased commit contains the same **change** as the original (compare the patches),
even though the IDs differ.

**Expected result.** The two patch IDs are equal. (`feature-tea@{1}` is the branch's previous position in its reflog:
the commit before the rebase.)

**Verification.**

<!-- test: output -->
```bash
cd ~/git-practice/lesson-60
git show 'feature-tea@{1}' | git patch-id | cut -c1-12
git show feature-tea | git patch-id | cut -c1-12
```

```text
a8a3c0bf8d69
a8a3c0bf8d69
```

## Break it

Rebase a branch that was **already pushed**, then push it:

<!-- test: fail; contains=[rejected]; output -->
```bash
git init -q --bare ../lesson-60-server.git && git remote add origin ../lesson-60-server.git
git push -q -u origin main feature-tea
git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Raise the espresso price" && git push -q
git switch -q feature-tea && git rebase -q main
git push 2>&1
```

```text
To ../lesson-60-server.git
 ! [rejected]        feature-tea -> feature-tea (non-fast-forward)
error: failed to push some refs to '../lesson-60-server.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

The server has the old `feature-tea` (with the old commit); your rebased branch does not contain it, so the push is
not a fast-forward and is rejected. Rebase **rewrote history** that someone else might already have.

The golden rule: **never rebase commits that others have built on.** Your own unshared commits, or your own feature
branch that only you use, are fine.

## Fix

It is Ada's own feature branch, nobody else works on it: replace it, safely.

<!-- test: contains=forced update; output -->
```bash
git push --force-with-lease 2>&1
```

```text
To ../lesson-60-server.git
 + a60fd19...af882cf feature-tea -> feature-tea (forced update)
```

## Real-world example

Before opening a PR, rebase your branch on the latest `main` (`git fetch && git rebase origin/main`): reviewers see
your commits on top of the current code, CI tests exactly what will be merged, and the history stays linear. After the
PR is open and others have commented, prefer merging `main` in, or use `--force-with-lease` and tell reviewers.

## Practice challenge

Rebase `feature-tea` back onto the original base commit `4267004` ("Add prices") using `--onto`, removing everything
`main` added from under it.

<details>
<summary>Solution</summary>

<!-- test: contains=4267004; output -->
```bash
cd ~/git-practice/lesson-60
git rebase -q --onto 4267004 main feature-tea
git log --oneline --graph -3
```

```text
* ad12083 (HEAD -> feature-tea) Add green tea to the menu
* 4267004 Add prices
* fc345e6 Add the menu
```

`git rebase --onto NEW OLD BRANCH` replays the commits of BRANCH after OLD onto NEW.

</details>

## Recap

- Rebase replays commits on a new base: same changes, new commits, new IDs.
- Linear history, but rewritten history: never rebase what others have built on.
- After rebasing your own pushed branch: `git push --force-with-lease`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-60 ~/git-practice/lesson-60-server.git
```

Next: [Lesson 61 · Basic rebase](../61-basic-rebase/README.md).
