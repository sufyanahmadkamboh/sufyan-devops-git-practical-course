# Lesson 15 · git diff

> Level 3 · Git history · ⏱ 20 minutes

## What are we learning?

How to compare any two versions: your edits, what is staged, two commits, two branches; and how to read the diff
format itself.

## Visual

```text
diff --git a/prices.txt b/prices.txt        ← which file
index 5813ff5..ddaed76 100644               ← blob IDs before..after, file mode
--- a/prices.txt                             ← "a" = the old side
+++ b/prices.txt                             ← "b" = the new side
@@ -1,3 +1,3 @@                              ← hunk: old lines 1-3, new lines 1-3
 espresso 2.50                               ← unchanged context line (starts with a space)
-latte 3.20                                  ← removed
+latte 3.30                                  ← added
 cappuccino 3.40
```

## Lab setup

<!-- test: contains=lesson-15 -->
```bash
bash scripts/new-lab.sh lesson-15 diverged
cd ~/git-practice/lesson-15
```

## Demonstration

A change in the working directory, then the three basic comparisons:

<!-- test: output -->
```bash
sed -i 's/latte 3.20/latte 3.30/' prices.txt
echo "chai" >> menu.txt && git add menu.txt
echo "=== git diff          (working directory vs staging area)"; git diff
echo "=== git diff --staged (staging area vs HEAD)";                git diff --staged
echo "=== git diff HEAD     (working directory vs HEAD)";           git diff HEAD --stat
```

```text
=== git diff          (working directory vs staging area)
diff --git a/prices.txt b/prices.txt
index 5813ff5..ddaed76 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,3 @@
 espresso 2.50
-latte 3.20
+latte 3.30
 cappuccino 3.40
=== git diff --staged (staging area vs HEAD)
diff --git a/menu.txt b/menu.txt
index 6c76265..45e2d15 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,3 +1,4 @@
 espresso
 latte
 cappuccino
+chai
=== git diff HEAD     (working directory vs HEAD)
 menu.txt   | 1 +
 prices.txt | 2 +-
 2 files changed, 2 insertions(+), 1 deletion(-)
```

Two commits, and two branches:

<!-- test: contains=+green tea; output -->
```bash
echo "=== HEAD~2 vs HEAD";             git diff HEAD~2 HEAD --stat
echo "=== main vs feature-tea";        git diff main feature-tea
echo "=== since feature-tea branched"; git diff main...feature-tea --stat
```

```text
=== HEAD~2 vs HEAD
 README.md  | 2 ++
 prices.txt | 3 +++
 2 files changed, 5 insertions(+)
=== main vs feature-tea
diff --git a/README.md b/README.md
index 742be8c..af07f28 100644
--- a/README.md
+++ b/README.md
@@ -1,5 +1,3 @@
 # Cafe
 
 The menu and prices of a small cafe.
-
-Open every day from 8:00 to 18:00.
diff --git a/menu.txt b/menu.txt
index 6c76265..cbd8549 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,3 +1,4 @@
 espresso
 latte
 cappuccino
+green tea
=== since feature-tea branched
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

`main feature-tea` compares the two tips: it shows the green tea added **and** the opening hours "removed" (they exist
only on `main`). `main...feature-tea` (three dots) compares feature-tea with the point where it branched off: only what
the branch itself changed. That is what a pull request shows.

## Command breakdown

| Command | Compares |
|---|---|
| `git diff` | working directory ↔ staging area |
| `git diff --staged` | staging area ↔ HEAD |
| `git diff HEAD` | working directory ↔ HEAD |
| `git diff A B` | commit/branch A ↔ commit/branch B |
| `git diff A...B` | B ↔ the merge base of A and B (the branch's own changes) |
| `git diff --stat` / `--name-only` | summary only |
| `git diff --word-diff` | changed words instead of whole lines |
| `git diff -- FILE` | limit to a file |

## Hands-on exercise

**Instructions.** Show the price change with `--word-diff` so only the changed number is highlighted.

**Expected result.** `latte [-3.20-]{+3.30+}`.

**Verification.**

<!-- test: contains=[-3.20-]{+3.30+} -->
```bash
cd ~/git-practice/lesson-15
git diff --word-diff prices.txt
```

## Break it

Compare against a branch name with a typo:

<!-- test: fail; contains=unknown revision; output -->
```bash
git diff main..featur-tea 2>&1
```

```text
fatal: ambiguous argument 'main..featur-tea': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

## Troubleshoot

`ambiguous argument 'featur-tea': unknown revision or path not in the working tree`: Git could not resolve the name
as a commit, branch, tag or file. List the real branch names:

<!-- test: contains=feature-tea -->
```bash
git branch --all
```

## Fix

<!-- test: contains=green tea -->
```bash
git diff main..feature-tea -- menu.txt
```

## Real-world example

Before approving a release: `git diff v1.2.0 v1.3.0 --stat` lists everything that changed between two releases;
`git diff v1.2.0 v1.3.0 -- helm/` limits it to the Helm chart. In a code review, `git diff main...feature` shows exactly
the branch's changes, the same view as the pull request page.

## Practice challenge

Without committing, prove whether your working directory differs from the `feature-tea` branch in `README.md`.

<details>
<summary>Solution</summary>

<!-- test: contains=Open every day; output -->
```bash
cd ~/git-practice/lesson-15
git diff feature-tea -- README.md
```

```text
diff --git a/README.md b/README.md
index af07f28..742be8c 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,5 @@
 # Cafe
 
 The menu and prices of a small cafe.
+
+Open every day from 8:00 to 18:00.
```

`git diff <commit>` compares that commit with your working directory. `main` has the opening hours, `feature-tea`
does not, so the README differs.

</details>

## Recap

- `git diff` (unstaged), `--staged` (to be committed), `HEAD` (both), `A B` (two commits), `A...B` (a branch's own changes).
- Lines starting with `-` were removed, `+` added, space = unchanged context; `@@` marks a hunk.
- `--stat`, `--name-only`, `--word-diff` and `-- FILE` shape the output.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-15
```

Next: [Lesson 16 · Commit history visualization](../16-history-visualization/README.md).
