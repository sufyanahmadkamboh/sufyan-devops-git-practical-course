# Lesson 29 · Undo working directory changes

> Level 6 · Undoing changes · ⏱ 15 minutes

## What are we learning?

How to throw away edits you have not staged yet: `git restore FILE`. And why this is one of the few Git commands that
really destroys work.

## Visual

```text
 Working directory      Staging area        Repository
 (your edits)           (index)             (last commit)
      │                      │
      │ ◄──── git restore FILE ─┘   copies the STAGED version over your file
      │                             (= the committed version, if nothing is staged)

 unstaged edits that are overwritten were never stored anywhere: they are gone.
```

## Lab setup

<!-- test: contains=lesson-29 -->
```bash
bash scripts/new-lab.sh lesson-29 basic
cd ~/git-practice/lesson-29
```

## Demonstration

An experiment that went wrong:

<!-- test: contains=M prices.txt; output -->
```bash
sed -i 's/2.50/25.00/' prices.txt
echo "free cookies" >> menu.txt
git status --short
```

```text
 M menu.txt
 M prices.txt
```

Throw away the change to `prices.txt` only:

<!-- test: contains=espresso 2.50; output -->
```bash
git restore prices.txt
git status --short
head -1 prices.txt
```

```text
 M menu.txt
espresso 2.50
```

`prices.txt` is back to the committed version; `menu.txt` still has its edit. Restore everything in the current folder:

<!-- test: contains=nothing to commit -->
```bash
git restore .
git status
```

## Command breakdown

| Command | What it does |
|---|---|
| `git restore FILE` | discard unstaged changes to FILE |
| `git restore .` | discard all unstaged changes below the current folder |
| `git restore -p FILE` | choose hunk by hunk what to discard |
| `git restore --source=COMMIT FILE` | take FILE as it was in COMMIT |
| `git checkout -- FILE` | the older command for the same thing |
| `git clean -n` / `-f` | new **untracked** files are not touched by restore: lesson 72 |

## Hands-on exercise

**Instructions.** Bring `prices.txt` back to how it was in the **first** commit that contained it, using `--source`.

**Expected result.** The file matches the commit `Add prices`, and `git status` shows it modified (if it differs) or
clean (if it is identical, as here).

**Verification.**

<!-- test: contains=latte 3.20 -->
```bash
cd ~/git-practice/lesson-29
git restore --source=4267004 prices.txt
cat prices.txt
```

## Break it

Restore the wrong file: a whole morning's work in `menu.txt`.

<!-- test: absent=flat white -->
```bash
printf 'flat white\ncortado\n' >> menu.txt
git restore menu.txt
cat menu.txt
```

## Troubleshoot

The two new lines are gone, and Git cannot bring them back: they were never staged or committed, so no object was ever
written (lesson 74). Look at the reflog, the stash list, the object store: nothing.

<!-- test: absent=cortado -->
```bash
git reflog | head -3
git stash list
git fsck --lost-found 2>/dev/null | head -3 || true
```

Your editor's undo history or local history (VS Code "Timeline", JetBrains "Local History") is the only hope.

## Fix

Prevention is the fix: anything worth keeping should be at least **staged** before you experiment. A staged version is
written as an object and survives a `restore` of the working directory:

<!-- test: contains=flat white; output -->
```bash
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
echo "a bad experiment" >> menu.txt
git restore menu.txt
cat menu.txt
```

```text
espresso
latte
cappuccino
flat white
cortado
```

`git restore` restored the **staged** version: the bad experiment is gone, the two staged lines are kept.

## Real-world example

You changed `values-prod.yaml` to debug a deployment and forgot. Before committing anything, `git status` shows
`M values-prod.yaml`; `git diff values-prod.yaml` shows exactly your debug change; `git restore values-prod.yaml`
removes it. Always read the diff before restoring, so you know what you are deleting.

## Practice challenge

You edited two parts of `prices.txt`. Keep one and discard the other, using `git restore -p`.

<details>
<summary>Solution</summary>

<!-- test: contains=espresso 2.60; absent=cappuccino 9; output -->
```bash
cd ~/git-practice/lesson-29
git restore --source=HEAD --staged --worktree .
sed -i 's/espresso 2.50/espresso 2.60/; s/cappuccino 3.40/cappuccino 9.99/' prices.txt
printf 's\nn\ny\n' | git restore -p prices.txt > /dev/null
cat prices.txt
```

```text
espresso 2.60
latte 3.20
cappuccino 3.40
```

The two edits are one hunk (lines close together), so `s` splits it; answer `n` (keep) for the espresso change and `y`
(discard) for the cappuccino one.

</details>

## Recap

- `git restore FILE` discards unstaged edits; they cannot be recovered.
- It restores the **staged** version if there is one, otherwise the committed one.
- Read `git diff` before restoring; stage what you want to keep.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-29
```

Next: [Lesson 30 · Unstage files](../30-unstage-files/README.md).
