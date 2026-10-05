# Lesson 62 · Rebase vs merge

> Level 13 · Rebase · ⏱ 20 minutes

## What are we learning?

Merge and rebase both integrate work; they produce different histories. We build both from the same starting point,
compare them, and see the one situation where rebase really hurts: rebasing a branch someone else has built on.

## Visual

```text
 same start:  main A ── B ── D        feature B ── C1 ── C2

 merge:   A ── B ── D ──────── M        + true record of what happened, nothing rewritten
                ╲            ╱           − extra merge commits, a busier graph
                 C1 ─── C2 ─

 rebase:  A ── B ── D ── C1' ── C2'     + linear, easy to read and bisect
                                        − rewrites commits: never on shared branches
```

## Lab setup

<!-- test: contains=lesson-62 -->
```bash
bash scripts/new-lab.sh lesson-62 diverged
cd ~/git-practice/lesson-62
git switch -q feature-tea && echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea" && git switch -q main
git branch merge-way main && git branch rebase-way feature-tea
```

## Demonstration

**Merge**:

<!-- test: contains=Merge branch 'feature-tea' into merge-way; output -->
```bash
git switch -q merge-way && git merge -q --no-edit feature-tea
git log --oneline --graph merge-way
```

```text
*   64d6f2a (HEAD -> merge-way) Merge branch 'feature-tea' into merge-way
|\  
| * b4e37a0 (rebase-way, feature-tea) Price green tea
| * bb67674 Add green tea to the menu
* | f40d080 (main) Add opening hours
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

**Rebase** (then fast-forward main-side):

<!-- test: absent=Merge; output -->
```bash
git switch -q rebase-way && git rebase -q main
git log --oneline --graph rebase-way
```

```text
* ca94f31 (HEAD -> rebase-way) Price green tea
* 15ac374 Add green tea to the menu
* f40d080 (main) Add opening hours
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Same content, different history:

<!-- test: contains=identical; output -->
```bash
git diff --quiet merge-way rebase-way && echo "identical files"
echo "merge-way: $(git rev-list --count merge-way) commits, rebase-way: $(git rev-list --count rebase-way) commits"
```

```text
identical files
merge-way: 7 commits, rebase-way: 6 commits
```

## Command breakdown

| Situation | Prefer |
|---|---|
| update your own unpushed / solo branch with main | rebase |
| integrate a finished feature into main | merge (or squash) via PR |
| a branch others have pulled or built on | merge |
| clean up your own commits before review | interactive rebase (lesson 63) |
| local commits vs teammates' on the same branch | `git pull --rebase` |

## Hands-on exercise

**Instructions.** Show only the merge commits of each branch.

**Expected result.** One on `merge-way`, none on `rebase-way`.

**Verification.**

<!-- test: contains=merge-way: 1; contains=rebase-way: 0 -->
```bash
cd ~/git-practice/lesson-62
for b in merge-way rebase-way; do echo "$b: $(git rev-list --merges --count "$b")"; done
```

## Break it

Ada pushes `feature-tea`; Grace builds on it; Ada then rebases and force-pushes. Grace pulls with a merge:

<!-- test: contains=Price green tea; output -->
```bash
git init -q --bare ../lesson-62-server.git && git remote add origin ../lesson-62-server.git
git push -q origin main feature-tea
git clone -q -b feature-tea ../lesson-62-server.git ../lesson-62-grace
(cd ../lesson-62-grace && git config user.name "Grace Hopper" && git config user.email grace@example.com &&
  echo "green tea is popular" > notes.txt && git add notes.txt && git commit -q -m "Add notes")
git switch -q feature-tea && git rebase -q main && git push -q --force-with-lease origin feature-tea
cd ../lesson-62-grace && git pull -q --no-rebase --no-edit
git log --oneline --graph | head -12
```

```text
*   f448256 (HEAD -> feature-tea) Merge branch 'feature-tea' of ~/git-practice/lesson-62/../lesson-62-server into feature-tea
|\  
| * 507d4af (origin/feature-tea) Price green tea
| * 0dda4da Add green tea to the menu
| * f40d080 (origin/main, origin/HEAD) Add opening hours
* | b2ed916 Add notes
* | b4e37a0 Price green tea
* | bb67674 Add green tea to the menu
|/  
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

## Troubleshoot

"Add green tea to the menu" and "Price green tea" now appear **twice** in Grace's history: the originals (which
Grace's commit is built on) and the rebased copies (from Ada's force push), joined by a merge. Merged into `main`, the
history would carry both.

<!-- test: contains=2; output -->
```bash
git log --oneline | grep -c "Price green tea"
```

```text
2
```

## Fix

Grace undoes her merge and **rebases** her own commit onto the new branch instead. Git recognises that the old copies
are already upstream (same patches) and skips them:

<!-- test: contains=1; output -->
```bash
git reset -q --hard ORIG_HEAD
git rebase origin/feature-tea 2>&1 | grep -v "^hint:" || true
git log --oneline | grep -c "Price green tea"
git log --oneline --graph | head -5
```

```text
warning: skipped previously applied commit bb67674
warning: skipped previously applied commit b4e37a0
Rebasing (1/1)
Successfully rebased and updated refs/heads/feature-tea.
1
* 3b7ba33 (HEAD -> feature-tea) Add notes
* 507d4af (origin/feature-tea) Price green tea
* 0dda4da Add green tea to the menu
* f40d080 (origin/main, origin/HEAD) Add opening hours
* 4267004 Add prices
```

Prevention: do not rebase branches others have pulled; if you must, tell them and have them use `git pull --rebase`.

## Real-world example

Many teams use both: developers rebase their own feature branches on `main` while they work (clean, linear, easy
review), and PRs are merged with a merge commit or squash, so `main` itself is never rewritten. `git config
--global rebase.updateRefs true` helps when you stack several branches on top of each other.

## Practice challenge

Show which commits Grace's branch and Ada's branch have in common by patch, even though their IDs differ.

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-62-grace
git fetch -q
git log --oneline --cherry-mark --left-right origin/main...HEAD
```

```text
> 3b7ba33 (HEAD -> feature-tea) Add notes
> 507d4af (origin/feature-tea) Price green tea
> 0dda4da Add green tea to the menu
```

`=` marks commits with an equivalent patch on the other side, `<`/`>` the ones unique to each side.

</details>

## Recap

- Merge records history as it happened; rebase rewrites it into a straight line.
- Same final files, different graphs.
- Rebasing a shared branch duplicates commits for everyone who built on it.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-62 ~/git-practice/lesson-62-server.git ~/git-practice/lesson-62-grace
```

Next: [Lesson 63 · Interactive rebase](../63-interactive-rebase/README.md).
