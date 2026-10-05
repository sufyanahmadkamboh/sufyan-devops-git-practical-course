# Lesson 14 · git show

> Level 3 · Git history · ⏱ 15 minutes

## What are we learning?

How to inspect one commit: its metadata and its changes, a summary of the files it touched, and a file exactly as it
was in that commit.

## Visual

```text
 git show COMMIT              git show --stat COMMIT       git show COMMIT:FILE
 ─────────────────            ──────────────────────       ────────────────────
 commit, author, date         commit, author, date         the whole file, as it was
 message                      message                      in that commit
 diff of every changed file   prices.txt | 1 +
```

Ways to name a commit: a hash (`4267004`), a branch (`main`), `HEAD`, `HEAD~1` (one before), `HEAD~3`, a tag (`v1.0`).

## Lab setup

<!-- test: contains=lesson-14 -->
```bash
bash scripts/new-lab.sh lesson-14 history
cd ~/git-practice/lesson-14
git log --oneline
```

## Demonstration

The latest commit, complete:

<!-- test: contains=+mocha 3.90; output -->
```bash
git show
```

```text
commit ecff18af63d0d85da66114f18c12b06e2ae9888b (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:07:00 2026 +0000

    Price mocha

diff --git a/prices.txt b/prices.txt
index cc9a276..82c50c8 100644
--- a/prices.txt
+++ b/prices.txt
@@ -2,3 +2,4 @@ espresso 2.50
 latte 3.20
 cappuccino 3.40
 green tea 2.80
+mocha 3.90
```

An older one, by position and as a summary:

<!-- test: contains=menu.txt | 1 +; output -->
```bash
git show --stat HEAD~3
```

```text
commit 68335807cd443a4434ab82646c84e5f26b37e0e2
Author: Ada Lovelace <ada@example.com>
Date:   Mon Jan 5 09:04:00 2026 +0000

    Add green tea

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
```

A file as it was three commits ago, without changing anything in your folder:

<!-- test: contains=cappuccino 3.40; absent=mocha; output -->
```bash
git show HEAD~3:prices.txt
```

```text
espresso 2.50
latte 3.20
cappuccino 3.40
```

## Command breakdown

| Command | Shows |
|---|---|
| `git show` | the latest commit (= `git show HEAD`) with its diff |
| `git show HASH` / `HEAD~N` / `BRANCH` | that commit |
| `git show --stat COMMIT` | files changed, insertions/deletions, no diff |
| `git show --name-only COMMIT` | only the file names |
| `git show COMMIT:PATH` | a file's content in that commit |
| `git show -s --format=... COMMIT` | metadata only, in your format |

## Hands-on exercise

**Instructions.** Show who wrote the commit that added green tea's price, and when, without its diff.

**Expected result.** One line with author and date.

**Verification.**

<!-- test: contains=Ada Lovelace -->
```bash
cd ~/git-practice/lesson-14
git show -s --format='%h %an %ad %s' "$(git log --format=%h --grep='Price green tea')"
```

## Break it

<!-- test: fail; contains=does not exist in; output -->
```bash
git show HEAD~4:hours.txt 2>&1
```

```text
fatal: path 'hours.txt' does not exist in 'HEAD~4'
```

## Troubleshoot

`path 'hours.txt' does not exist in 'HEAD~4'`: the file did not exist in that commit (or the path is wrong). List what
was in that snapshot:

<!-- test: contains=menu.txt -->
```bash
git show --name-only --format= HEAD~4
git ls-tree --name-only HEAD~4
```

## Fix

Ask for a file that existed in that commit:

<!-- test: contains=latte -->
```bash
git show HEAD~4:menu.txt
```

## Real-world example

During an incident: "what exactly did yesterday's deployment change?" `git show --stat <deployed-commit>` lists the
files; `git show <commit>:k8s/deployment.yaml` shows the manifest exactly as deployed, even if `main` has moved on since.

## Practice challenge

Show only the names of the files changed by the last three commits together, each name once.

<details>
<summary>Solution</summary>

<!-- test: contains=prices.txt; output -->
```bash
cd ~/git-practice/lesson-14
git diff --name-only HEAD~3 HEAD
```

```text
menu.txt
prices.txt
```

Comparing the snapshot from three commits ago with the latest gives the combined list (`git show` shows commits one
at a time).

</details>

## Recap

- `git show COMMIT` = metadata + diff of one commit; `--stat` and `--name-only` summarise.
- `COMMIT:PATH` prints a file as it was in that commit.
- Commits can be named by hash, branch, tag, `HEAD`, `HEAD~N`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-14
```

Next: [Lesson 15 · git diff](../15-git-diff/README.md).
