# Lesson 40 · git fetch

> Level 8 · Remote repositories · ⏱ 15 minutes

## What are we learning?

`git fetch` downloads new commits from the remote and updates `origin/*`, **without touching your branches or files**.
It is the safe way to see what changed before you integrate it.

## Visual

```text
 before fetch:   main, origin/main → B          server: main → D (Grace pushed C and D)

 git fetch:      downloads C, D; moves origin/main → D
                 main stays at B; your files are unchanged

                 A ── B  ← main
                       ╲
                        C ── D  ← origin/main     "behind 2"
```

## Lab setup

<!-- test: contains=lesson-40 -->
```bash
bash scripts/new-lab.sh lesson-40 remote
cd ~/git-practice/lesson-40/grace
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git push -q
cd ../ada
```

Grace pushed two commits. We are Ada.

## Demonstration

<!-- test: contains=-> origin/main; output -->
```bash
git fetch
```

```text
From ~/git-practice/lesson-40/server/cafe
   4267004..9755f90  main       -> origin/main
```

<!-- test: contains=behind 'origin/main' by 2 commits; output -->
```bash
git status
git log --oneline main..origin/main
```

```text
On branch main
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
9755f90 (origin/main, origin/HEAD) Price green tea
0284799 Add green tea
```

`main..origin/main` = "commits on `origin/main` that are not on `main`": exactly what a pull would bring in. Review
them before integrating:

<!-- test: contains=+green tea 2.80; output -->
```bash
git diff main origin/main
```

```text
diff --git a/menu.txt b/menu.txt
index 6c76265..cbd8549 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,3 +1,4 @@
 espresso
 latte
 cappuccino
+green tea
diff --git a/prices.txt b/prices.txt
index 5813ff5..cc9a276 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,4 @@
 espresso 2.50
 latte 3.20
 cappuccino 3.40
+green tea 2.80
```

## Command breakdown

| Command | What it does |
|---|---|
| `git fetch` | fetch from `origin` (all branches) |
| `git fetch REMOTE` / `--all` | a specific remote / all remotes |
| `git fetch --prune` | also delete `origin/*` branches removed on the server |
| `git log main..origin/main` | incoming commits |
| `git log origin/main..main` | outgoing commits (yours, not pushed) |
| `git status` | ahead/behind summary (after a fetch) |

## Hands-on exercise

**Instructions.** Integrate the fetched commits into Ada's `main` without contacting the server again.

**Expected result.** A fast-forward; `main` and `origin/main` at the same commit.

<!-- test-run: cd ~/git-practice/lesson-40/ada && git merge -q origin/main -->

**Verification.**

<!-- test: contains=up to date with 'origin/main' -->
```bash
cd ~/git-practice/lesson-40/ada
git status
```

## Break it

Grace deletes a branch on the server; Ada's clone keeps showing it:

<!-- test: contains=origin/old-promo; output -->
```bash
cd ../grace && git push -q origin main:old-promo && cd ../ada && git fetch -q
cd ../grace && git push -q origin --delete old-promo && cd ../ada
git fetch
git branch -r
```

```text
  origin/HEAD -> origin/main
  origin/main
  origin/old-promo
```

## Troubleshoot

`origin/old-promo` is stale: a plain fetch adds and updates remote-tracking branches but never deletes them. On busy
repositories this produces dozens of dead `origin/*` branches.

<!-- test: contains=stale; output -->
```bash
git remote show origin | grep -i stale
```

```text
    refs/remotes/origin/old-promo stale (use 'git remote prune' to remove)
```

## Fix

<!-- test: contains=[deleted]; output -->
```bash
git fetch --prune
git branch -r
```

```text
From ~/git-practice/lesson-40/server/cafe
 - [deleted]         (none)     -> origin/old-promo
  origin/HEAD -> origin/main
  origin/main
```

Make it permanent: `git config --global fetch.prune true`.

## Real-world example

Before starting work in the morning: `git fetch`, then `git status` and `git log --oneline main..origin/main`. You see
exactly what your colleagues merged overnight, review it, and merge or rebase deliberately, instead of being surprised
by a `git pull` that conflicts.

## Practice challenge

Make a commit on Ada's `main` without pushing, fetch, and show both the incoming and the outgoing commits.

<details>
<summary>Solution</summary>

<!-- test: contains=Ada's unpushed note; output -->
```bash
cd ~/git-practice/lesson-40/ada
echo "note" > notes.txt && git add notes.txt && git commit -q -m "Ada's unpushed note"
git fetch -q
echo "incoming:"; git log --oneline main..origin/main
echo "outgoing:"; git log --oneline origin/main..main
```

```text
incoming:
outgoing:
0f9f559 (HEAD -> main) Ada's unpushed note
```

</details>

## Recap

- `git fetch` updates `origin/*` only; your branches and files are untouched.
- `main..origin/main` incoming, `origin/main..main` outgoing.
- `--prune` (or `fetch.prune true`) removes branches deleted on the server.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-40
```

Next: [Lesson 41 · git pull](../41-git-pull/README.md).
