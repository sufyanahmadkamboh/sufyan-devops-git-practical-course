# Lesson 56 · Feature branch workflow

> Level 12 · Collaboration · ⏱ 20 minutes

## What are we learning?

The feature branch workflow in detail: naming, keeping the branch up to date with `main` while it lives, and why
long-lived branches hurt.

## Visual

```text
 main     A ── B ───────── C ─────── D ──────────── M
               ╲                     ╲             ╱
 feature/x      f1 ── f2 ──────────── U ── f3 ────     U = "update from main" (merge or rebase)
               short-lived: days, not weeks; updated when main moves
```

Naming conventions (pick one per team): `feature/menu-tea`, `fix/latte-price`, `docs/opening-hours`,
`chore/update-chart`, optionally with an issue number: `feature/42-menu-tea`.

## Lab setup

<!-- test: contains=lesson-56 -->
```bash
bash scripts/new-lab.sh lesson-56 remote
cd ~/git-practice/lesson-56/ada
```

## Demonstration

Ada starts a feature from the latest `main`:

<!-- test: contains=feature/menu-tea -->
```bash
git switch -q main && git pull -q
git switch -c feature/menu-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea to the menu"
git push -q -u origin feature/menu-tea
```

Meanwhile Grace's change lands on `main`:

<!-- test: contains=Fix the latte price -->
```bash
(cd ../grace && sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price" && git push -q)
git fetch -q && git log --oneline -1 origin/main
```

Ada updates her branch with `main`, tests, and continues:

<!-- test: contains=latte 3.30; output -->
```bash
git merge -q --no-edit origin/main
git log --oneline --graph -5
grep latte prices.txt
```

```text
*   8790654 (HEAD -> feature/menu-tea) Merge remote-tracking branch 'origin/main' into feature/menu-tea
|\  
| * 3161720 (origin/main, origin/HEAD) Fix the latte price
* | b6aa139 (origin/feature/menu-tea) Add green tea to the menu
|/  
* 4267004 (main) Add prices
* fc345e6 Add the menu
latte 3.30
```

## Command breakdown

| Step | Commands |
|---|---|
| start | `git switch main && git pull && git switch -c feature/NAME` |
| save + share | `git commit`, `git push -u origin feature/NAME` |
| update from main | `git fetch && git merge origin/main` (or `git rebase origin/main`, lesson 61) |
| finish | PR → review → merge → `git switch main && git pull && git branch -d feature/NAME` |

## Hands-on exercise

**Instructions.** List the remote feature branches and how far each is behind `origin/main`.

**Expected result.** `feature/menu-tea` 0 behind (it was just updated).

**Verification.**

<!-- test: contains=origin/feature/menu-tea 0 behind -->
```bash
cd ~/git-practice/lesson-56/ada
git push -q
for b in $(git branch -r --format='%(refname:short)' | grep feature/); do echo "$b $(git rev-list --count "$b..origin/main") behind"; done
```

## Break it

A long-lived branch: Grace starts `feature/new-prices`, works on it for "three weeks" without updating, while `main`
keeps changing the same file:

<!-- test: fail; contains=CONFLICT; output -->
```bash
cd ~/git-practice/lesson-56/grace && git pull -q
git switch -q -c feature/new-prices
sed -i 's/espresso 2.50/espresso 2.70/; s/cappuccino 3.40/cappuccino 3.60/' prices.txt && git commit -q -am "New prices"
cd ../ada && git switch -q main && git merge -q feature/menu-tea && git pull -q --no-rebase --no-edit
for p in 2.55 2.60 2.65; do sed -i "s/^espresso .*/espresso $p/" prices.txt && git commit -q -am "Espresso $p" && git push -q; done
cd ../grace && git fetch -q && git merge origin/main 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

## Troubleshoot

Three weeks of `main` against three weeks of branch: the longer they diverge, the more overlapping changes, the
harder the conflict, and the less anyone remembers why each change was made.

<!-- test: output -->
```bash
git rev-list --left-right --count HEAD...origin/main | awk '{print "branch has", $1, "own commit(s); main has", $2, "new commit(s)"}'
git merge --abort
```

```text
branch has 1 own commit(s); main has 5 new commit(s)
```

## Fix

Resolve once (keep the new prices for both items), then keep the branch fresh: merge `main` in every day, or after
every merged PR that touches the same area.

<!-- test: contains=espresso 2.70; output -->
```bash
git merge origin/main > /dev/null 2>&1 || true
git checkout --ours prices.txt && git add prices.txt && git commit -q --no-edit
head -1 prices.txt
```

```text
Updated 1 path from the index
espresso 2.70
```

## Real-world example

Trunk-based teams keep branches under a day or two and hide unfinished features behind **feature flags** instead of
keeping them on a branch: the code is merged early, switched off in production. Long-lived branches are what produce
"merge week" before a release.

## Practice challenge

Write a one-liner that lists remote branches whose last commit is older than 14 days (stale branches to clean up).

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-56/ada
git fetch -q
git for-each-ref refs/remotes/origin --format='%(committerdate:unix) %(refname:short)' |
  awk -v limit="$(( $(date +%s) - 14*24*3600 ))" '$1 < limit {print $2}'
```

```text
```

Branches created by the lab script's fixed 2026-01-05 commits (such as `origin/main` before today's work) would appear;
everything committed today does not.

</details>

## Recap

- One short-lived branch per task, named by convention.
- Update the branch from `main` regularly; conflicts stay small.
- Long-lived branches = big conflicts; prefer small PRs and feature flags.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-56
```

Next: [Lesson 57 · GitHub Flow](../57-github-flow/README.md).
