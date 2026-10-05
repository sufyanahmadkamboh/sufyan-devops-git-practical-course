# Lesson 01 · What is Git?

> Level 1 · Git fundamentals · ⏱ 15 minutes · run every command from the course folder (`git-practical-course/`)

## What are we learning?

Why version control exists, by first working **without** it, then doing the same work with Git and comparing.

## Visual

```text
Without Git                                  With Git

project-final                                Commit 1  "Add the menu"
project-final2                                  ↓
project-final-final                          Commit 2  "Add prices"
project-final-final-v2                          ↓
project-final-real          ← which one?     Commit 3  "Raise the latte price"   ← who, when, why: recorded
```

Git is a **version control system**: it records snapshots of your project (commits), who made each one, when, and
why, and it can show the difference between any two of them or bring any of them back.

## Lab setup

A practice folder, outside the course folder. Every lesson works in `~/git-practice/`:

<!-- test: contains=lesson-01 -->
```bash
mkdir -p ~/git-practice/lesson-01/without-git
cd ~/git-practice/lesson-01
pwd
```

## Demonstration

First, the way many people start: copies with new names.

<!-- test: output -->
```bash
cd without-git
printf 'espresso 2.50\nlatte 3.20\n' > prices-final.txt
cp prices-final.txt prices-final2.txt && printf 'cappuccino 3.40\n' >> prices-final2.txt
cp prices-final2.txt prices-final-final.txt && sed -i 's/latte 3.20/latte 3.30/' prices-final-final.txt
ls
```

```text
prices-final-final.txt
prices-final.txt
prices-final2.txt
```

Three files. Which one is current? What changed between `final2` and `final-final`, and why? Who changed the latte price?
The folder cannot answer. Now the same three steps with Git:

<!-- test: contains=Raise the latte price; output -->
```bash
cd ~/git-practice/lesson-01
mkdir with-git && cd with-git
git init -q -b main
git config user.name "Ada Lovelace" && git config user.email "ada@example.com"
printf 'espresso 2.50\nlatte 3.20\n' > prices.txt
git add prices.txt && git commit -q -m "Add prices"
printf 'cappuccino 3.40\n' >> prices.txt
git add prices.txt && git commit -q -m "Add cappuccino"
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add prices.txt && git commit -q -m "Raise the latte price"
git log --oneline
```

```text
0a9b8c0 (HEAD -> main) Raise the latte price
218782d Add cappuccino
6f74527 Add prices
```

One file, three recorded versions. Ask Git what the last change was:

<!-- test: contains=-latte 3.20; contains=+latte 3.30; output -->
```bash
git show --stat --format='%h %an %ad%n%s' --date=short HEAD
git diff HEAD~1 HEAD
```

```text
0a9b8c0 Ada Lovelace 2026-10-05
Raise the latte price

 prices.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
diff --git a/prices.txt b/prices.txt
index 5813ff5..ddaed76 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,3 @@
 espresso 2.50
-latte 3.20
+latte 3.30
 cappuccino 3.40
```

The commit knows its author, its date, its message, and exactly which line changed: `-latte 3.20`, `+latte 3.30`.
And the old version is one command away:

<!-- test: contains=latte 3.20; output -->
```bash
git show HEAD~2:prices.txt
```

```text
espresso 2.50
latte 3.20
```

## Command breakdown

| Command | What it does here |
|---|---|
| `git init -q -b main` | turn the current folder into a Git repository, first branch `main` (`-q`: quietly) |
| `git config user.name/email` | who you are, written into every commit (lesson 04 does this properly) |
| `git add prices.txt` | choose what goes into the next snapshot |
| `git commit -m "..."` | record the snapshot with a message |
| `git log --oneline` | the history, one line per commit |
| `git diff HEAD~1 HEAD` | what changed between the previous commit and the latest |
| `git show HEAD~2:prices.txt` | the file as it was two commits ago |

## Hands-on exercise

**Instructions.** In `~/git-practice/lesson-01/with-git`, add a fourth version: put `mocha 3.90` in `prices.txt` and
commit it with the message `Add mocha`.

**Expected result.** `git log --oneline` shows four commits, the newest on top.

**Verification.**

<!-- test-run: cd ~/git-practice/lesson-01/with-git && printf 'mocha 3.90\n' >> prices.txt && git add prices.txt && git commit -q -m "Add mocha" -->

<!-- test: contains=Add mocha -->
```bash
cd ~/git-practice/lesson-01/with-git
git log --oneline | head -1
git log --oneline | wc -l
```

## Break it

Delete the file, as if by accident:

<!-- test: contains=deleted -->
```bash
cd ~/git-practice/lesson-01/with-git
rm prices.txt
ls; git status --short; echo "(prices.txt deleted)"
```

## Troubleshoot

`git status` (lesson 08) shows ` D prices.txt`: Git noticed the file is gone. In the no-Git folder, a deleted file is
simply gone. Here, every committed version still exists inside the repository.

## Fix

<!-- test: contains=mocha 3.90; output -->
```bash
git restore prices.txt
cat prices.txt
```

```text
espresso 2.50
latte 3.30
cappuccino 3.40
mocha 3.90
```

## Real-world example

A teammate asks "why did the latte price change in March?". With copies, someone has to remember. With Git:
`git log -p -- prices.txt` lists every change to the file, with the author, date and message of each. Every DevOps
repository works this way: application code, Dockerfiles, Kubernetes manifests, Helm charts, CI pipelines.

## Practice challenge

Without opening the file, print the content of `prices.txt` as it was in the **first** commit, and show which lines
were added between the first and the latest commit.

<details>
<summary>Solution</summary>

<!-- test: contains=+cappuccino 3.40; output -->
```bash
cd ~/git-practice/lesson-01/with-git
first=$(git rev-list --max-parents=0 HEAD)
git show "$first":prices.txt
git diff "$first" HEAD
```

```text
espresso 2.50
latte 3.20
diff --git a/prices.txt b/prices.txt
index df45f17..051d8e7 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,2 +1,4 @@
 espresso 2.50
-latte 3.20
+latte 3.30
+cappuccino 3.40
+mocha 3.90
```

`git rev-list --max-parents=0 HEAD` finds the root commit (the one with no parent). Lessons 13–15 cover history and
diffs in depth.

</details>

## Recap

- Git records **snapshots** (commits) with author, date and message.
- Any version can be compared with any other, and brought back.
- Copies named `final-final` cannot tell you what changed, who changed it, or why.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-01
```

Next: [Lesson 02 · Git vs GitHub](../02-git-vs-github/README.md).
