# Lesson 07 · The working directory

> Level 2 · Repositories · ⏱ 15 minutes

## What are we learning?

The working directory is where you edit files. Git compares it with the last commit and tells you what is new,
modified or deleted. We create, change and delete files and watch how Git sees each one.

## Visual

```text
 last commit (HEAD)          working directory              what Git reports
 ──────────────────          ─────────────────              ────────────────
 menu.txt  (3 lines)    vs   menu.txt  (4 lines)       →    modified
 prices.txt             vs   (gone)                    →    deleted
 (not there)            vs   hours.txt                 →    untracked (new, never committed)
 README.md              =    README.md                 →    (nothing: unchanged files are not listed)
```

## Lab setup

<!-- test: contains=lesson-07 -->
```bash
bash scripts/new-lab.sh lesson-07 basic
cd ~/git-practice/lesson-07
```

## Demonstration

Clean to start with: the working directory matches the last commit.

<!-- test: contains=nothing to commit, working tree clean; output -->
```bash
git status
```

```text
On branch main
nothing to commit, working tree clean
```

Now three kinds of change at once:

<!-- test: output -->
```bash
echo "green tea" >> menu.txt                 # modify a tracked file
rm prices.txt                                # delete a tracked file
echo "Open 8-18" > hours.txt                 # create a new file
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   menu.txt
	deleted:    prices.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	hours.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Git sorts them: `modified: menu.txt` and `deleted: prices.txt` under *Changes not staged for commit*, `hours.txt` under
*Untracked files*. Nothing is recorded yet: the commit history has not changed. What exactly changed in `menu.txt`?

<!-- test: contains=+green tea; output -->
```bash
git diff menu.txt
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
```

## Command breakdown

| Command | What it does |
|---|---|
| `git status` | compare the working directory (and staging area) with the last commit |
| `git status --short` | the same, one line per file: ` M` modified, ` D` deleted, `??` untracked |
| `git diff FILE` | the line-by-line changes not yet staged |

## Hands-on exercise

**Instructions.** Rename `README.md` to `INFO.md` with plain `mv` and look at `git status --short`.

**Expected result.** Git shows the old name as deleted and the new name as untracked. It recognises a rename only once
both sides are staged (lesson 09: `git add -A` then shows `R`).

<!-- test-run: cd ~/git-practice/lesson-07 && mv README.md INFO.md -->

**Verification.**

<!-- test: contains=D README.md; contains=?? INFO.md -->
```bash
cd ~/git-practice/lesson-07
git status --short
```

## Break it

You worked for an hour and want everything back the way it was, so you delete the folder's files by hand and copy
old ones from somewhere. Simulate a simpler version: you edited a file and now want the committed version, but you
type the wrong command:

<!-- test: fail; contains=pathspec; output -->
```bash
git restore menu.text 2>&1
```

```text
error: pathspec 'menu.text' did not match any file(s) known to git
```

## Troubleshoot

`pathspec 'menu.text' did not match any file(s) known to git`: the path is wrong (`.text` instead of `.txt`). Git can
only restore paths it knows. List what it tracks:

<!-- test: contains=menu.txt -->
```bash
git ls-files
```

## Fix

<!-- test: contains=R  README.md -> INFO.md; output -->
```bash
git restore menu.txt prices.txt
git add -A && git status --short
```

```text
R  README.md -> INFO.md
A  hours.txt
```

`menu.txt` and `prices.txt` are back to their committed content. And after `git add -A`, the rename from the exercise
is recognised: `R README.md -> INFO.md`.

## Real-world example

Before you start any task, `git status` should say *working tree clean*. Before you commit, `git status` tells you
exactly which files you touched: a stray debug file or a modified config you did not mean to change shows up here
first, not in production.

## Practice challenge

Make `git status --short` show exactly one modified file and one untracked file, and nothing else.

<details>
<summary>Solution</summary>

<!-- test: contains= M menu.txt; contains=?? specials.txt; output -->
```bash
cd ~/git-practice/lesson-07
git restore --staged . && git restore . && rm -f INFO.md hours.txt && git checkout -q -- README.md 2>/dev/null; git status --short
echo "chai" >> menu.txt
echo "Monday: 2 for 1" > specials.txt
git status --short
```

```text
 M menu.txt
?? specials.txt
```

</details>

## Recap

- The working directory is your files as they are right now; Git compares them with the last commit.
- Three states for a changed file: modified, deleted, untracked.
- Nothing is recorded until you commit; `git restore` brings back the committed version of a file.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-07
```

Next: [Lesson 08 · git status](../08-git-status/README.md).
