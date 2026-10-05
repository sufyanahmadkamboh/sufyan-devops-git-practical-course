# Lesson 21 · Branch visualization

> Level 4 · Branches · ⏱ 15 minutes

## What are we learning?

Watching branches move: each commit moves the **current** branch's label forward, and only that one. We build a small
history one commit at a time and draw it after every step.

## Visual

```text
 1. start             2. commit on feature        3. commit on main

 A─B  main, feature   A─B  main                    A─B──D  main
                         ╲                            ╲
                          C  feature                   C  feature
```

## Lab setup

<!-- test: contains=lesson-21 -->
```bash
bash scripts/new-lab.sh lesson-21 basic
cd ~/git-practice/lesson-21
```

## Demonstration

Step 1, a branch at the same commit as `main`:

<!-- test: contains=feature; output -->
```bash
git branch feature
git log --oneline --graph --all
```

```text
* 4267004 (HEAD -> main, feature) Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Step 2, a commit on `feature`: only the `feature` label moves.

<!-- test: contains=(HEAD -> feature); output -->
```bash
git switch -q feature
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --graph --all
```

```text
* 85afb8e (HEAD -> feature) Add green tea
* 4267004 (main) Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Step 3, a commit on `main`: now the history forks.

<!-- test: contains=|/; output -->
```bash
git switch -q main
echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add hours"
git log --oneline --graph --all
```

```text
* 85afb8e (feature) Add green tea
| * 21c291f (HEAD -> main) Add hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Command breakdown

| Command | Use |
|---|---|
| `git log --oneline --graph --all` | the drawing used in every step |
| `git log --graph --all --format='%h %d %s'` | the same with labels only where they are |
| `git rev-parse main feature` | the commit each label points to |
| `git merge-base main feature` | the commit where they forked (lesson 25) |

## Hands-on exercise

**Instructions.** Find the commit where `main` and `feature` forked.

**Expected result.** `4267004`, the "Add prices" commit.

**Verification.**

<!-- test: contains=4267004 -->
```bash
cd ~/git-practice/lesson-21
git merge-base main feature | cut -c1-7
```

## Break it

Commit on the wrong branch: you meant to add the chai recipe to `feature`, but you are on `main`.

<!-- test: contains=Add chai -->
```bash
echo "chai: black tea, spices, milk" > chai.txt && git add chai.txt && git commit -q -m "Add chai"
git log --oneline --graph --all | head -4
```

## Troubleshoot

The graph shows `Add chai` under the `HEAD -> main` label: the label that moved is the one `HEAD` was on. Committing
always moves the current branch.

## Fix

Move the commit: put it on `feature` (cherry-pick, lesson 67), then take it off `main` (reset, lesson 31; safe here
because `main` was never pushed):

<!-- test: contains=Add chai; output -->
```bash
git switch -q feature
git cherry-pick main > /dev/null
git switch -q main
git reset -q --hard HEAD~1
git log --oneline --graph --all
```

```text
* 63edaa0 (feature) Add chai
* 85afb8e Add green tea
| * 21c291f (HEAD -> main) Add hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Real-world example

Most "my commit disappeared" or "why is this commit on main?" questions are about which label moved. Shell prompts that
show the current branch (Git Bash does it by default; `__git_ps1` or tools like starship elsewhere) prevent most of them.

## Practice challenge

Make the graph show **three** tips: `main`, `feature` and a new `experiment` branch that forks from `feature`.

<details>
<summary>Solution</summary>

<!-- test: contains=experiment; output -->
```bash
cd ~/git-practice/lesson-21
git switch -q -c experiment feature
echo "oat milk" >> menu.txt && git commit -q -am "Try oat milk"
git log --oneline --graph --all
```

```text
* 06becd2 (HEAD -> experiment) Try oat milk
* 63edaa0 (feature) Add chai
* 85afb8e Add green tea
| * 21c291f (main) Add hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

</details>

## Recap

- A commit moves only the branch `HEAD` is on.
- Branches fork when two of them get different new commits; `git merge-base` finds the fork point.
- Draw the graph often; it answers most "where did my commit go" questions.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-21
```

Next: [Lesson 22 · Deleting branches](../22-deleting-branches/README.md).
