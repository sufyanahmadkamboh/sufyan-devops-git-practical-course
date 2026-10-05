# Lesson 16 · Commit history visualization

> Level 3 · Git history · ⏱ 20 minutes

## What are we learning?

How to see history as what it really is: a graph of commits pointing to their parents, with branches as labels on
some of them. We draw it, then build one and compare.

## Visual

```text
 linear history                  a branch                         a merge

 D  ← main (HEAD)                    C ← feature                      M ← main
 │                               B ──┘                              ╱  ╲
 C                               │                                 C    D
 │                               A                                 ╲  ╱
 B                                                                   B
 │                               each commit points to its          │
 A                               PARENT (arrows go back in time)     A
```

A commit has one parent (normal), two parents (a merge), or none (the first commit).

## Lab setup

<!-- test: contains=lesson-16 -->
```bash
bash scripts/new-lab.sh lesson-16 diverged
cd ~/git-practice/lesson-16
```

## Demonstration

The lab has two branches that each moved on after splitting:

<!-- test: contains=feature-tea; output -->
```bash
git log --oneline --graph --all
```

```text
* f40d080 (HEAD -> main) Add opening hours
| * bb67674 (feature-tea) Add green tea to the menu
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Read it bottom-up: three shared commits, then the history splits. `main` has "Add opening hours", `feature-tea` has
"Add green tea". Now merge them and draw again:

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
git merge -q --no-edit feature-tea
git log --oneline --graph --all
```

```text
*   2267cc4 (HEAD -> main) Merge branch 'feature-tea'
|\  
| * bb67674 (feature-tea) Add green tea to the menu
* | f40d080 Add opening hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

The merge commit has **two** parents. Ask Git for each commit's parents:

<!-- test: output -->
```bash
git log --format='%h  parents: %p  %s' -5
```

```text
2267cc4  parents: f40d080 bb67674  Merge branch 'feature-tea'
f40d080  parents: 4267004  Add opening hours
bb67674  parents: 4267004  Add green tea to the menu
4267004  parents: fc345e6  Add prices
fc345e6  parents: d6df412  Add the menu
```

Readable alternatives: `git log --graph --all --format='%h %d %s (%an, %ar)'`, `gitk --all` (a window), the network or
commit graph views on GitHub, or your editor's Git panel. They all draw the same graph.

## Command breakdown

| Command | What it draws |
|---|---|
| `git log --oneline --graph --all` | the whole graph, every branch |
| `git log --graph --decorate --format='%h %d %s'` | with branch and tag labels (`%d`) |
| `git log --format='%h %p'` | each commit and its parents |
| `git log --first-parent` | only the main line, skipping the merged-in commits |
| `git show-branch` | a compact branch comparison |

## Hands-on exercise

**Instructions.** Show only the main line of history, the way a release manager sees it: merges, not the commits that
came from branches.

**Expected result.** The merge commit appears, `Add green tea` does not.

**Verification.**

<!-- test: contains=Merge branch; absent=Add green tea -->
```bash
cd ~/git-practice/lesson-16
git log --oneline --first-parent
```

## Break it

Draw the graph without `--all` from the side branch and conclude, wrongly, that `main` has nothing new:

<!-- test: absent=Merge branch; output -->
```bash
git switch -q feature-tea
git log --oneline --graph
```

```text
* bb67674 (HEAD -> feature-tea) Add green tea to the menu
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Troubleshoot

Without `--all`, `git log` draws only what is reachable from `HEAD`. From `feature-tea`, the opening hours and the
merge on `main` are invisible, although they exist. Same lesson as lesson 13: a view is not the whole repository.

## Fix

<!-- test: contains=Merge branch -->
```bash
git log --oneline --graph --all
git switch -q main
```

## Real-world example

Before rebasing or merging a long-lived branch, draw `git log --oneline --graph --all` (or with `main..feature` and
`feature..main` counts: `git rev-list --left-right --count main...feature`) to see how far the branches have diverged.
A branch 300 commits behind `main` is a conversation with the team before it is a command.

## Practice challenge

How many commits does `main` have that `feature-tea` does not, and the other way round? Answer with one command.

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-16
git rev-list --left-right --count main...feature-tea
```

```text
2	0
```

Left number: commits only on `main` (the opening hours and the merge); right: only on `feature-tea` (0: it has been
merged, so everything it has is on `main` too).

</details>

## Recap

- History is a graph: commits point to their parents; branches are labels on commits.
- `git log --oneline --graph --all` draws the whole graph; `--first-parent` follows the main line.
- A merge commit has two parents; the first commit has none.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-16
```

Next: [Module 05 · Lesson 17 · Why branches exist](../../05-branches/17-why-branches/README.md).
