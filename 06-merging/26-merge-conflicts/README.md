# Lesson 26 · Merge conflicts

> Level 5 · Merging · ⏱ 20 minutes

## What are we learning?

What a merge conflict is, why it happens, and how to read the conflict markers Git writes into the file.

## Visual

```text
 base:      latte 3.20
 main:      latte 3.30   (Grace)
 feature:   latte 3.50   (Ada)
                 ↓ the same line changed differently on both sides: Git cannot choose

 prices.txt after git merge:

 espresso 2.50
 <<<<<<< HEAD                 ← start: the version of the branch you are ON (main)
 latte 3.30
 =======                      ← separator
 latte 3.50
 >>>>>>> feature-tea          ← end: the version of the branch you are MERGING
 cappuccino 3.40
```

## Lab setup

<!-- test: contains=lesson-26 -->
```bash
bash scripts/new-lab.sh lesson-26 conflict
cd ~/git-practice/lesson-26
git log --oneline --graph --all
```

## Demonstration

<!-- test: fail; contains=CONFLICT (content): Merge conflict in prices.txt; output -->
```bash
git merge feature-tea
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

The merge stopped. Look at the file:

<!-- test: contains=<<<<<<< HEAD; output -->
```bash
cat prices.txt
```

```text
espresso 2.50
<<<<<<< HEAD
latte 3.30
=======
latte 3.50
>>>>>>> feature-tea
cappuccino 3.40
```

Everything outside the markers merged fine (`espresso`, `cappuccino`); only the contested line is marked. The base
version can be shown too, which makes the decision easier ("what did it say before both changes?"):

<!-- test: contains=||||||| ; output -->
```bash
git checkout --conflict=diff3 prices.txt
cat prices.txt
```

```text
Recreated 1 merge conflict
espresso 2.50
<<<<<<< ours
latte 3.30
||||||| base
latte 3.20
=======
latte 3.50
>>>>>>> theirs
cappuccino 3.40
```

`|||||||` introduces the merge base's version: `latte 3.20`. So main raised it to 3.30 and feature to 3.50.

## Command breakdown

| Marker / command | Meaning |
|---|---|
| `<<<<<<< HEAD` | start of the current branch's version ("ours") |
| `\|\|\|\|\|\|\| base` | the common ancestor's version (with `diff3`/`zdiff3` style) |
| `=======` | separator |
| `>>>>>>> branch` | end of the merged branch's version ("theirs") |
| `git checkout --conflict=diff3 FILE` | re-write the markers including the base |
| `git config merge.conflictStyle zdiff3` | always show the base (recommended) |

## Hands-on exercise

**Instructions.** Find out from Git (not by reading the file) which files are in conflict.

**Expected result.** `prices.txt`.

**Verification.**

<!-- test: contains=prices.txt -->
```bash
cd ~/git-practice/lesson-26
git diff --name-only --diff-filter=U
```

## Break it

Ignore the conflict and try to commit:

<!-- test: fail; contains=unmerged; output -->
```bash
git commit -m "Merge" 2>&1
```

```text
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U	prices.txt
```

## Troubleshoot

`Committing is not possible because you have unmerged files.`: Git will not record a merge while a file is still in
conflict. `git status` explains where you are:

<!-- test: contains=both modified; output -->
```bash
git status
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

## Fix

Resolution is lesson 27. For now, step back out of the merge (lesson 28):

<!-- test: contains=nothing to commit -->
```bash
git merge --abort
git status
```

## Real-world example

Two engineers bump the same image tag in `values-prod.yaml` on different branches: one to `1.4.1` (a hotfix), one to
`1.5.0` (the next release). Git cannot know which is right: that decision needs a human who understands both changes.
A conflict is Git asking a question, not an error in Git.

## Practice challenge

Set `zdiff3` as your conflict style globally, recreate the conflict, and show that the base appears automatically.

<details>
<summary>Solution</summary>

<!-- test: contains=||||||| ; output -->
```bash
cd ~/git-practice/lesson-26
git config --global merge.conflictStyle zdiff3
git merge feature-tea > /dev/null 2>&1 || true
cat prices.txt
git merge --abort
```

```text
espresso 2.50
<<<<<<< HEAD
latte 3.30
||||||| 4267004
latte 3.20
=======
latte 3.50
>>>>>>> feature-tea
cappuccino 3.40
```

`zdiff3` is `diff3` with identical lines at the edges moved out of the conflict: a smaller conflict to read.

</details>

## Recap

- A conflict = the same lines changed differently on both sides; Git stops and asks you.
- `<<<<<<< HEAD` (yours) / `=======` / `>>>>>>> branch` (theirs); `|||||||` shows the base.
- You cannot commit until every conflict is resolved; `git status` lists them as "both modified".

## Cleanup

<!-- test -->
```bash
cd ~
git config --global --unset merge.conflictStyle
rm -rf ~/git-practice/lesson-26
```

(The course's labs show the default conflict style, so the setting is removed here; keep `zdiff3` in your own
configuration afterwards if you like it.)

Next: [Lesson 27 · Resolving merge conflicts](../27-resolving-conflicts/README.md).
