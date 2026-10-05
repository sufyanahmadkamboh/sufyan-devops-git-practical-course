# Lesson 20 · Create and switch in one command

> Level 4 · Branches · ⏱ 10 minutes

## What are we learning?

`git switch -c NAME` creates a branch and switches to it: the command you will use to start almost every piece of
work. And starting it from the right place.

## Visual

```text
 git switch -c feature-login           =   git branch feature-login + git switch feature-login

 A ── B ── C  ← main
            ↖ feature-login (HEAD)      ← new label on the current commit, and HEAD on it
```

## Lab setup

<!-- test: contains=lesson-20 -->
```bash
bash scripts/new-lab.sh lesson-20 diverged
cd ~/git-practice/lesson-20
```

## Demonstration

<!-- test: contains=Switched to a new branch 'feature-login'; output -->
```bash
git switch -c feature-login
git branch
```

```text
Switched to a new branch 'feature-login'
* feature-login
  feature-tea
  main
```

The new branch starts at the commit you were on. You can choose another starting point instead:

<!-- test: contains=Switched to a new branch 'fix-tea-price'; output -->
```bash
git switch -c fix-tea-price feature-tea
git log --oneline -1
```

```text
Switched to a new branch 'fix-tea-price'
bb67674 (HEAD -> fix-tea-price, feature-tea) Add green tea to the menu
```

The older equivalent is `git checkout -b NAME [START]`.

## Command breakdown

| Command | What it does |
|---|---|
| `git switch -c NAME` | create NAME at the current commit and switch to it |
| `git switch -c NAME START` | create it at START (a branch, tag or commit) |
| `git switch -C NAME` | create, or reset an existing NAME to here (overwrites: careful) |
| `git checkout -b NAME` | the older equivalent |

## Hands-on exercise

**Instructions.** Start a branch `feature-hours` from `main` (wherever you are now), with one commit adding
`hours.txt`.

**Expected result.** `feature-hours` is one commit ahead of `main`.

<!-- test-run: cd ~/git-practice/lesson-20 && git switch -q -c feature-hours main && echo "8-18" > hours.txt && git add hours.txt && git commit -q -m "Add hours" -->

**Verification.**

<!-- test: contains=Add hours -->
```bash
cd ~/git-practice/lesson-20
git log --oneline main..feature-hours
```

## Break it

The most common mistake: starting a new branch from the **wrong** branch. You are on `fix-tea-price` and start a new
feature from here without noticing:

<!-- test: contains=Add green tea to the menu; output -->
```bash
git switch -q fix-tea-price
git switch -c feature-specials
echo "Monday special" > specials.txt && git add specials.txt && git commit -q -m "Add specials"
git log --oneline main..feature-specials
```

```text
Switched to a new branch 'feature-specials'
5d6c90c (HEAD -> feature-specials) Add specials
bb67674 (fix-tea-price, feature-tea) Add green tea to the menu
```

## Troubleshoot

`main..feature-specials` should show only "Add specials", but it also contains "Add green tea to the menu": the new
branch inherited everything from the branch it started on. Always check where you are (`git branch --show-current`)
before `git switch -c`, or name the start point explicitly.

## Fix

Rebuild the branch from `main` with only its own commit (lesson 61 explains `rebase --onto`):

<!-- test: contains=Add specials; absent=green tea; output -->
```bash
git rebase -q --onto main fix-tea-price feature-specials
git log --oneline main..feature-specials
```

```text
3485fa5 (HEAD -> feature-specials) Add specials
```

## Real-world example

Starting work in a team: `git switch main && git pull && git switch -c feature/JIRA-42-cache-headers` (lesson 41 for
`pull`). The habit of starting from an up-to-date `main` avoids both "my branch contains someone else's unmerged work"
and "my branch is already 50 commits behind".

## Practice challenge

Create `release-test` from the commit **two before** the tip of `main`, in one command.

<details>
<summary>Solution</summary>

<!-- test: contains=Add the menu; output -->
```bash
cd ~/git-practice/lesson-20
git switch -c release-test main~2
git log --oneline -1
```

```text
Switched to a new branch 'release-test'
fc345e6 (HEAD -> release-test) Add the menu
```

</details>

## Recap

- `git switch -c NAME [START]` creates and switches in one step.
- A new branch contains everything of its starting point: start from the right place.
- `--onto` (lesson 61) repairs a branch started from the wrong place.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-20
```

Next: [Lesson 21 · Branch visualization](../21-branch-visualization/README.md).
