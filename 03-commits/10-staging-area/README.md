# Lesson 10 · The staging area

> Level 2 · Commits · ⏱ 20 minutes

## What are we learning?

Why Git has a staging area between your files and your commits, and how to see what is in it with
`git diff` and `git diff --staged`.

## Visual

```text
 Working Directory  ──git add──►  Staging Area  ──git commit──►  Repository (HEAD)
         │                             │                              │
         └──── git diff ───────────────┘                              │
                                       └──── git diff --staged ───────┘
         └──────────────────────── git diff HEAD ─────────────────────┘
```

The staging area lets you **build a commit from part of your changes**: two unrelated changes in your folder become
two separate, clean commits.

## Lab setup

<!-- test: contains=lesson-10 -->
```bash
bash scripts/new-lab.sh lesson-10 basic
cd ~/git-practice/lesson-10
```

## Demonstration

Two unrelated changes: a typo fix in the README and a new menu item.

<!-- test: output -->
```bash
sed -i 's/small cafe/small, friendly cafe/' README.md
echo "green tea" >> menu.txt
git status --short
```

```text
 M README.md
 M menu.txt
```

Stage only the README fix. Now ask both questions:

<!-- test: contains=+green tea; contains=friendly; output -->
```bash
git add README.md
echo "=== git diff (working directory vs staging area: NOT staged)"
git diff
echo "=== git diff --staged (staging area vs last commit: WILL be committed)"
git diff --staged
```

```text
=== git diff (working directory vs staging area: NOT staged)
diff --git a/menu.txt b/menu.txt
index 6c76265..cbd8549 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,3 +1,4 @@
 espresso
 latte
 cappuccino
+green tea
=== git diff --staged (staging area vs last commit: WILL be committed)
diff --git a/README.md b/README.md
index af07f28..6ddc00a 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,3 @@
 # Cafe
 
-The menu and prices of a small cafe.
+The menu and prices of a small, friendly cafe.
```

Commit the staged part only, then the rest as a second commit:

<!-- test: contains=Add green tea; contains=Describe the cafe; output -->
```bash
git commit -q -m "Describe the cafe"
git add menu.txt && git commit -q -m "Add green tea"
git log --oneline -3
```

```text
943de56 (HEAD -> main) Add green tea
c1c57e9 Describe the cafe
4267004 Add prices
```

Two focused commits from one working session. Each can be reviewed, reverted or cherry-picked on its own.

## Command breakdown

| Command | Compares |
|---|---|
| `git diff` | working directory ↔ staging area (unstaged changes) |
| `git diff --staged` (= `--cached`) | staging area ↔ last commit (what the next commit contains) |
| `git diff HEAD` | working directory ↔ last commit (everything, staged or not) |
| `git diff --stat` | the same, summarised per file |

## Hands-on exercise

**Instructions.** Change both `prices.txt` (raise the espresso to 2.60) and `menu.txt` (add `chai`). Stage only the
price change, and prove with the two diffs which change will be committed.

**Expected result.** `git diff --staged` shows only `espresso`; `git diff` shows only `chai`.

<!-- test-run: cd ~/git-practice/lesson-10 && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && echo chai >> menu.txt && git add prices.txt -->

**Verification.**

<!-- test: contains=+espresso 2.60; contains=+chai -->
```bash
cd ~/git-practice/lesson-10
git diff --staged | grep '^[+-][a-z]'
git diff | grep '^[+-][a-z]'
```

## Break it

Commit and expect everything to be in it, without checking:

<!-- test: contains=M menu.txt -->
```bash
git commit -q -m "Update espresso price and add chai"
git status --short
```

## Troubleshoot

The message says "and add chai" but `git status` still shows ` M menu.txt`: `chai` was never staged, so the commit
contains only the price. The commit message now lies about the commit.

<!-- test: absent=chai; output -->
```bash
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

```text
-espresso 2.50
+espresso 2.60
```

## Fix

The commit is not pushed, so it may be changed: stage the missing part and amend the last commit (lesson 11):

<!-- test: contains=+chai; output -->
```bash
git add menu.txt
git commit -q --amend --no-edit
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

```text
+chai
-espresso 2.50
+espresso 2.60
```

## Real-world example

Reviewers read commits. A commit called "Fix the readiness probe" that also changes an unrelated image tag hides a
risky change inside a harmless-looking one. The staging area is the tool that keeps each commit honest: one purpose,
one commit.

## Practice challenge

Put two changes **in the same file** into two different commits: add `chai` at the end of `menu.txt` and change
`espresso` to `ristretto` at the top, then commit them separately. (Hint: `git add -p`, answering `y`/`n` per hunk.)

<details>
<summary>Solution</summary>

<!-- test: contains=Rename espresso; contains=Add mocha; output -->
```bash
cd ~/git-practice/lesson-10
printf 'ristretto\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git diff
# git add -p asks about each hunk. Both edits are close together, so Git shows them as ONE hunk:
# "s" splits it, then "y" stages the first part and "n" skips the second.
printf 's\ny\nn\n' | git add -p menu.txt > /dev/null
git commit -q -m "Rename espresso to ristretto"
git add menu.txt && git commit -q -m "Add mocha"
git log --oneline -2
```

```text
diff --git a/menu.txt b/menu.txt
index 02e91d0..52d5b90 100644
--- a/menu.txt
+++ b/menu.txt
@@ -1,5 +1,6 @@
-espresso
+ristretto
 latte
 cappuccino
 green tea
 chai
+mocha
97cd3f4 (HEAD -> main) Add mocha
8d52e67 Rename espresso to ristretto
```

`git add -p` splits a file's changes into hunks and asks for each one (`y` yes, `n` no, `s` split, `q` quit, `?`
help); that is how one file's changes end up in two commits.

</details>

## Recap

- The staging area is the draft of the next commit.
- `git diff` = not staged; `git diff --staged` = will be committed; `git diff HEAD` = everything.
- Stage deliberately to keep commits focused; check `git diff --staged` before committing.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-10
```

Next: [Lesson 11 · git commit](../11-git-commit/README.md).
