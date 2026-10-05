# Lesson 17 · Why branches exist

> Level 4 · Branches · ⏱ 15 minutes

## What are we learning?

The problem branches solve: several pieces of work in progress at once, without stepping on each other or on the
stable version. We feel the problem first, on a single branch.

## Visual

```text
 one branch for everything                  a branch per piece of work

 main ← Developer A (half-done login)        main  (always releasable)
      ← Developer B (half-done payments)       ├── feature-login     ← A works here
      ← Developer C (urgent bug fix)           ├── feature-payments  ← B works here
 → nothing on main is ever releasable          └── bugfix-prices     ← C fixes, merges, ships
```

## Lab setup

<!-- test: contains=lesson-17 -->
```bash
bash scripts/new-lab.sh lesson-17 basic        # one branch for everything
bash scripts/new-lab.sh lesson-17b basic       # the same project, with branches
cd ~/git-practice/lesson-17
```

## Demonstration

Work on a new feature, directly on `main`, half finished:

<!-- test: output -->
```bash
echo "loyalty card: 10th coffee free (WORK IN PROGRESS)" >> README.md
git commit -q -am "WIP: loyalty card"
git log --oneline
```

```text
b5c10db (HEAD -> main) WIP: loyalty card
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

Now an urgent request arrives: the latte price is wrong and must be fixed and released **now**. But `main` contains a
half-finished feature. Fixing on `main` ships the unfinished work along with the fix:

<!-- test: contains=WIP; output -->
```bash
sed -i 's/latte 3.20/latte 3.10/' prices.txt
git commit -q -am "Fix the latte price"
git log --oneline -2
```

```text
f9c4227 (HEAD -> main) Fix the latte price
b5c10db WIP: loyalty card
```

Whatever we release from `main` now contains "WIP: loyalty card". The same work with a branch for the feature:

<!-- test: contains=feature-loyalty; output -->
```bash
cd ~/git-practice/lesson-17b
git switch -q -c feature-loyalty
echo "loyalty card: 10th coffee free (WORK IN PROGRESS)" >> README.md
git commit -q -am "WIP: loyalty card"
git switch -q main
sed -i 's/latte 3.20/latte 3.10/' prices.txt
git commit -q -am "Fix the latte price"
git log --oneline --graph --all
```

```text
* 7e32ef1 (feature-loyalty) WIP: loyalty card
| * 18c8f11 (HEAD -> main) Fix the latte price
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

`main` has the fix and **only** the fix: releasable. The loyalty work waits on its own branch until it is done.

## Command breakdown

| Command | What it does |
|---|---|
| `git switch -c NAME` | create a branch here and switch to it (lesson 20) |
| `git switch NAME` | switch to an existing branch (lesson 19) |
| `git log --oneline --graph --all` | see every branch at once |

## Hands-on exercise

**Instructions.** In `lesson-17b`, finish the loyalty feature on its branch (remove `(WORK IN PROGRESS)`) without
touching `main`.

**Expected result.** `feature-loyalty` has two commits that `main` does not have; `main` is unchanged.

<!-- test-run: cd ~/git-practice/lesson-17b && git switch -q feature-loyalty && sed -i 's/ (WORK IN PROGRESS)//' README.md && git commit -q -am "Finish the loyalty card" && git switch -q main -->

**Verification.**

<!-- test: contains=Finish the loyalty card -->
```bash
cd ~/git-practice/lesson-17b
git log --oneline main..feature-loyalty
```

## Break it

Back in the single-branch lab: the release manager wants to ship the latte fix without the loyalty work. On one
branch, the two are in a line; you cannot take one without the other.

<!-- test: contains=WIP -->
```bash
cd ~/git-practice/lesson-17
git log --oneline main
```

## Troubleshoot

The history is linear: `Fix the latte price` sits on top of `WIP: loyalty card`. Releasing the commit with the fix
means releasing everything below it.

## Fix

Undo the mix-up the way a team would: move the unfinished work to its own branch, and rebuild `main` with only the fix
(lesson 67 explains `cherry-pick`; here it copies the fix):

<!-- test: absent=WIP; output -->
```bash
cd ~/git-practice/lesson-17
fix=$(git rev-parse HEAD)                    # remember the fix commit (the latest one)
git branch feature-loyalty HEAD~1            # a branch that keeps the WIP commit
git reset -q --hard HEAD~2                   # main back to before the WIP (lesson 31)
git cherry-pick "$fix" > /dev/null           # copy only the fix onto main
git log --oneline main
```

```text
35f851e (HEAD -> main) Fix the latte price
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

## Real-world example

In a DevOps repository, branches keep `main` deployable at all times: a half-finished Helm chart change lives on
`feature/helm-hpa`, a hotfix for production lives on `hotfix/readiness-probe`, and CI deploys only from `main`. No one
has to say "don't release yet, my change is half done".

## Practice challenge

Start two features at the same time from `main` in `lesson-17b` (`feature-a` and `feature-b`, one commit each) and
show that neither contains the other's commit.

<details>
<summary>Solution</summary>

<!-- test: contains=feature-a; contains=feature-b; output -->
```bash
cd ~/git-practice/lesson-17b
git switch -q -c feature-a main && echo a > a.txt && git add a.txt && git commit -q -m "Feature A"
git switch -q -c feature-b main && echo b > b.txt && git add b.txt && git commit -q -m "Feature B"
git log --oneline --graph feature-a feature-b main
```

```text
* 5ae7060 (feature-a) Feature A
| * 6d0e1b3 (HEAD -> feature-b) Feature B
|/  
* 18c8f11 (main) Fix the latte price
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Both branch off `main`; each has its own commit; neither sees the other.

</details>

## Recap

- One branch for everything means nothing is ever releasable on its own.
- A branch per piece of work keeps `main` stable and lets work happen in parallel.
- Branches are cheap: create them for every feature, fix and experiment.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-17 ~/git-practice/lesson-17b
```

Next: [Lesson 18 · Creating branches](../18-creating-branches/README.md).
