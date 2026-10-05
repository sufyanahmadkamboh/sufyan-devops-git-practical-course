# Lesson 34 · What is a stash?

> Level 7 · Stash · ⏱ 15 minutes

## What are we learning?

The stash is a shelf for unfinished work. `git stash` puts your uncommitted changes aside and gives you a clean
working directory, so you can switch to something urgent and come back later.

## Visual

```text
 working directory: half-finished feature          git stash
 ──────────────────────────────────────────        ──────────►   working directory: clean (= HEAD)
                                                                  stash@{0}: WIP on main: ...   ← your work, on the shelf

 ... fix the urgent bug, commit ...

                                                    git stash pop
                                                    ◄──────────   your half-finished work is back
```

## Lab setup

<!-- test: contains=lesson-34 -->
```bash
bash scripts/new-lab.sh lesson-34 basic
cd ~/git-practice/lesson-34
```

## Demonstration

You are halfway through adding a new drink:

<!-- test: contains=M menu.txt; output -->
```bash
echo "flat white" >> menu.txt
echo "flat white 3.60" >> prices.txt
git status --short
```

```text
 M menu.txt
 M prices.txt
```

Urgent: the espresso price on `main` is wrong and must be fixed **now**, without your half-finished work in the commit.

<!-- test: contains=stash@{0}; contains=nothing to commit; output -->
```bash
git stash
git stash list
git status
```

```text
Saved working directory and index state WIP on main: 4267004 Add prices
stash@{0}: WIP on main: 4267004 Add prices
On branch main
nothing to commit, working tree clean
```

The folder is clean. Fix and commit the urgent change:

<!-- test: contains=Fix the espresso price -->
```bash
sed -i 's/espresso 2.50/espresso 2.40/' prices.txt
git commit -q -am "Fix the espresso price"
git log --oneline -1
```

Take the work back from the shelf:

<!-- test: contains=flat white 3.60; contains=espresso 2.40; output -->
```bash
git stash pop
cat prices.txt
```

```text
Auto-merging prices.txt
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   menu.txt
	modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (754dde1c58ee39fbddf382f8693dd5ab01e2c936)
espresso 2.40
latte 3.20
cappuccino 3.40
flat white 3.60
```

Both are there: the committed fix and your unfinished work on top of it.

## Command breakdown

| Command | What it does |
|---|---|
| `git stash` | shelve tracked changes (staged and unstaged); clean working directory |
| `git stash list` | what is on the shelf |
| `git stash pop` | re-apply the latest stash and remove it from the shelf |
| `git stash -u` | also stash untracked (new) files |

## Hands-on exercise

**Instructions.** Stash your current work again, confirm the folder is clean, then pop it.

**Expected result.** After the stash: `git status` clean; after pop: `flat white` back in `menu.txt`.

<!-- test-run: cd ~/git-practice/lesson-34 && git stash -q && git status --short | wc -l | grep -qx 0 && git stash pop -q -->

**Verification.**

<!-- test: contains=flat white -->
```bash
cd ~/git-practice/lesson-34
grep "flat white" menu.txt
git stash list | wc -l
```

## Break it

Stash when your work includes a **new** file:

<!-- test: contains=?? specials.txt; output -->
```bash
echo "Monday: free cookie" > specials.txt
git stash
git status --short
```

```text
Saved working directory and index state WIP on main: 8c1f1e8 Fix the espresso price
?? specials.txt
```

## Troubleshoot

The modified tracked files were stashed, but `specials.txt` is still there: by default `git stash` ignores
**untracked** files. If you now switch branches or reset, the new file travels with you or gets in the way.

## Fix

Pop the stash, then stash again with `-u` (include untracked):

<!-- test: contains=nothing to commit; output -->
```bash
git stash pop -q
git stash -u
git status
git stash pop -q
```

```text
Saved working directory and index state WIP on main: 8c1f1e8 Fix the espresso price
On branch main
nothing to commit, working tree clean
```

## Real-world example

You are mid-way through a feature when production alerts. `git stash -u`, `git switch main`, `git pull`, create a
`hotfix/...` branch, fix, push, open a PR. Then `git switch feature`, `git stash pop`: back exactly where you were.
For anything longer than a few hours, prefer a "WIP" commit on your branch: stashes are local and easy to forget.

## Practice challenge

Is a stash pushed with `git push`? Find out by inspecting what a stash really is.

<details>
<summary>Solution</summary>

<!-- test: contains=refs/stash; output -->
```bash
cd ~/git-practice/lesson-34
git stash -q
git show-ref | grep stash
git log --oneline -1 stash
git stash pop -q
```

```text
b772b00c744a1737f6368305820a13d2af328644 refs/stash
b772b00 (refs/stash) WIP on main: 8c1f1e8 Fix the espresso price
```

A stash is a special commit stored under `refs/stash`, a local reference. `git push` sends branches and tags, never
`refs/stash`: stashes stay on your computer.

</details>

## Recap

- `git stash` shelves uncommitted work and cleans the working directory; `git stash pop` brings it back.
- Untracked files need `git stash -u`.
- Stashes are local commits under `refs/stash`; they are never pushed.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-34
```

Next: [Lesson 35 · Stash, apply and pop](../35-stash-apply-pop/README.md).
