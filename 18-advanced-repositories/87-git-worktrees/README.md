# Lesson 87 · Git worktrees

> Level 18 · Advanced repositories · ⏱ 20 minutes

## What are we learning?

A worktree is an extra working directory attached to the same repository. Instead of stashing your half-finished
feature to fix an urgent bug, you open the bug fix in a second folder, on another branch, at the same time. One
repository, several checked-out branches.

## Visual

```text
 lesson-87/            (main worktree)     branch feature-tea   ← half-finished work stays as it is
 ├── .git/             the ONE repository (objects, refs, config)
 lesson-87-hotfix/     (linked worktree)   branch hotfix        ← urgent fix, in parallel
 lesson-87-review/     (linked worktree)   detached at origin/… ← review a colleague's branch

 rule: a branch can be checked out in only one worktree at a time
```

## Lab setup

<!-- test: contains=lesson-87 -->
```bash
bash scripts/new-lab.sh lesson-87 feature
cd ~/git-practice/lesson-87
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt
git status --short
```

You are in the middle of the feature (uncommitted change in `prices.txt`) when an urgent price bug is reported.

## Demonstration

Open a second working directory for the hotfix, without touching the current one:

<!-- test: contains=lesson-87-hotfix; output -->
```bash
git worktree add -b hotfix ../lesson-87-hotfix main
git worktree list
```

```text
Preparing worktree (new branch 'hotfix')
HEAD is now at 4267004 Add prices
~/git-practice/lesson-87        bb67674 [feature-tea]
~/git-practice/lesson-87-hotfix 4267004 [hotfix]
```

Fix and commit there:

<!-- test: contains=Fix the espresso price -->
```bash
cd ../lesson-87-hotfix
sed -i 's/espresso 2.50/espresso 2.40/' prices.txt && git commit -q -am "Fix the espresso price"
git log --oneline -1
```

Back in the feature folder, the uncommitted work is untouched, and the new commit is visible (same repository):

<!-- test: contains=M prices.txt; contains=Fix the espresso price; output -->
```bash
cd ../lesson-87
git status --short
git log --oneline -1 hotfix
```

```text
 M prices.txt
510e333 (hotfix) Fix the espresso price
```

## Command breakdown

| Command | What it does |
|---|---|
| `git worktree add PATH BRANCH` | new working directory on an existing branch |
| `git worktree add -b NEW PATH START` | … on a new branch |
| `git worktree add --detach PATH REV` | … detached (review, builds) |
| `git worktree list` | all worktrees |
| `git worktree remove PATH` | delete a worktree (refuses if it has changes) |
| `git worktree prune` | forget worktrees whose folders were deleted manually |

## Hands-on exercise

**Instructions.** Merge the hotfix into `main` from the main worktree... `main` is not checked out anywhere, so do it
from the hotfix worktree: switch it to `main` and merge.

**Expected result.** `main` contains "Fix the espresso price".

<!-- test-run: cd ~/git-practice/lesson-87-hotfix && git switch -q main && git merge -q hotfix -->

**Verification.**

<!-- test: contains=Fix the espresso price -->
```bash
cd ~/git-practice/lesson-87
git log --oneline -1 main
```

## Break it

Try to check out `main` in the main worktree as well:

<!-- test: fail; contains=is already used by worktree; output -->
```bash
git switch main 2>&1
```

```text
fatal: 'main' is already used by worktree at '~/git-practice/lesson-87-hotfix'
```

## Troubleshoot

`fatal: 'main' is already used by worktree at '…/lesson-87-hotfix'`: two folders on the same branch would each
move it independently. Git allows each branch in one worktree only.

## Fix

Finish with the hotfix worktree and remove it; then `main` is free:

<!-- test: contains=main; output -->
```bash
git stash -q
git worktree remove ../lesson-87-hotfix
git worktree list
git switch -q main && git branch --show-current
git switch -q feature-tea && git stash pop -q
```

```text
~/git-practice/lesson-87 bb67674 [feature-tea]
main
```

## Real-world example

Worktrees shine for: reviewing a PR while keeping your own work open (`git worktree add --detach ../review
origin/feature-x`), running a long test suite on one branch while coding on another, and keeping a `release/2.x`
checkout next to `main` for backports. They share one object store, so they are much cheaper than a second clone and
fetches update all of them.

## Practice challenge

Delete a worktree folder with `rm -rf` (as people often do), then clean up Git's records.

<details>
<summary>Solution</summary>

<!-- test: absent=lesson-87-review; output -->
```bash
cd ~/git-practice/lesson-87
git worktree add -q --detach ../lesson-87-review main
rm -rf ../lesson-87-review
git worktree prune
git worktree list
```

```text
~/git-practice/lesson-87 bb67674 [feature-tea]
```

</details>

## Recap

- A worktree is another working directory of the same repository, on another branch.
- No stashing or second clone needed to work on two things at once.
- One branch per worktree; `git worktree remove` / `prune` to clean up.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-87 ~/git-practice/lesson-87-hotfix ~/git-practice/lesson-87-review
```

Next: [Lesson 88 · Git LFS](../88-git-lfs/README.md).
