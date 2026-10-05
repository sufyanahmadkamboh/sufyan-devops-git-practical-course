# Lesson 23 · What is a merge?

> Level 5 · Merging · ⏱ 15 minutes

## What are we learning?

Merging brings the work of one branch into another. We see the two shapes a merge can produce, and that merging
**into** the current branch is always the direction.

## Visual

```text
 before                              after git merge feature (on main)

 main                                main
  │                                   │
  A                                   A
  │                                   │
  B                                   B ─────── M   ← a merge commit with TWO parents: B and C
   ╲                                   ╲       ╱
    C  ← feature                        C ────     ← feature still points here
```

`git merge X` means "bring X into the branch I am on". `HEAD`'s branch moves; `X` does not.

## Lab setup

<!-- test: contains=lesson-23 -->
```bash
bash scripts/new-lab.sh lesson-23 diverged
cd ~/git-practice/lesson-23
git log --oneline --graph --all
```

## Demonstration

On `main`, merge `feature-tea`:

<!-- test: contains=Merge made by the 'ort' strategy; output -->
```bash
git switch -q main
git merge --no-edit feature-tea
```

```text
Merge made by the 'ort' strategy.
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

`ort` is Git's default merge strategy. The result:

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
git log --oneline --graph --all
cat menu.txt README.md
```

```text
*   b328274 (HEAD -> main) Merge branch 'feature-tea'
|\  
| * bb67674 (feature-tea) Add green tea to the menu
* | f40d080 Add opening hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
espresso
latte
cappuccino
green tea
# Cafe

The menu and prices of a small cafe.

Open every day from 8:00 to 18:00.
```

`main` now has both changes: green tea (from `feature-tea`) and the opening hours (from `main`). `feature-tea` did not
move. The merge commit has two parents:

<!-- test: output -->
```bash
git log -1 --format='%h parents: %p'
```

```text
b328274 parents: f40d080 bb67674
```

## Command breakdown

| Command | What it does |
|---|---|
| `git merge BRANCH` | bring BRANCH's commits into the current branch |
| `git merge --no-edit BRANCH` | accept the default merge message |
| `git merge -m "msg" BRANCH` | your own merge message |
| `git log --merges` | only merge commits |

## Hands-on exercise

**Instructions.** Find all merge commits in the lab's history.

**Expected result.** One: `Merge branch 'feature-tea'`.

**Verification.**

<!-- test: contains=Merge branch 'feature-tea' -->
```bash
cd ~/git-practice/lesson-23
git log --oneline --merges
```

## Break it

Merge in the wrong direction: you meant to bring `main` into your feature branch, but you are on `main`.

<!-- test: contains=Already up to date; output -->
```bash
git merge feature-tea
```

```text
Already up to date.
```

## Troubleshoot

`Already up to date.`: `main` already contains everything of `feature-tea` (the merge you just did). The direction
matters: `git merge X` changes the **current** branch. To update `feature-tea` with `main`'s latest work, you must be
**on** `feature-tea`.

## Fix

<!-- test: contains=Fast-forward; output -->
```bash
git switch -q feature-tea
git merge main
git log --oneline -1
```

```text
Updating bb67674..b328274
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
b328274 (HEAD -> feature-tea, main) Merge branch 'feature-tea'
```

`feature-tea` now has `main`'s work too. (It was a fast-forward: lesson 24.)

## Real-world example

On GitHub, merging a pull request is exactly `git merge feature` executed on `main` by GitHub. Updating a long-running
feature branch with the latest `main` (`git switch feature && git merge main`) is how you find integration problems
early, on your branch, rather than after merging.

## Practice challenge

Create two new branches from `main`, each adding a different new file, and merge both into `main`. How many merge
commits do you get?

<details>
<summary>Solution</summary>

<!-- test: contains=Merge branch 'b'; output -->
```bash
cd ~/git-practice/lesson-23
git switch -q main
git switch -q -c a && echo a > a.txt && git add a.txt && git commit -q -m "Add a"
git switch -q main && git switch -q -c b && echo b > b.txt && git add b.txt && git commit -q -m "Add b"
git switch -q main
git merge -q --no-edit a
git merge -q --no-edit b
git log --oneline --graph -6
```

```text
*   c0f8604 (HEAD -> main) Merge branch 'b'
|\  
| * 035eb43 (b) Add b
* | a18d378 (a) Add a
|/  
*   b328274 (feature-tea) Merge branch 'feature-tea'
|\  
| * bb67674 Add green tea to the menu
* | f40d080 Add opening hours
|/  
```

The first merge is a fast-forward (no merge commit, `main` had not moved); the second needs a merge commit, because
`main` now has `Add a`, which `b` does not have.

</details>

## Recap

- `git merge X` brings X into the current branch; the current branch moves, X does not.
- A merge commit has two parents and combines both histories.
- Check `git branch --show-current` before merging: direction matters.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-23
```

Next: [Lesson 24 · Fast-forward merge](../24-fast-forward/README.md).
