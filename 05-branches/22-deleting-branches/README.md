# Lesson 22 · Deleting branches

> Level 4 · Branches · ⏱ 15 minutes

## What are we learning?

How to delete branches safely with `-d`, why Git sometimes refuses, and when (and how carefully) to force it with `-D`.

## Visual

```text
 git branch -d feature        merged into the current branch? → label removed, commits stay (they are on main)
                              NOT merged?                     → refused: its commits would be unreachable

 git branch -D feature        removes the label anyway; unmerged commits become unreachable
                              (recoverable for a while with git reflog, lesson 79)
```

## Lab setup

<!-- test: contains=lesson-22 -->
```bash
bash scripts/new-lab.sh lesson-22 feature
cd ~/git-practice/lesson-22
git switch -q -c experiment && echo "oat milk" >> menu.txt && git commit -q -am "Try oat milk" && git switch -q main
git log --oneline --graph --all
```

## Demonstration

`feature-tea` is not merged yet. Merge it, then delete it:

<!-- test: contains=Deleted branch feature-tea; output -->
```bash
git merge -q feature-tea
git branch --merged
git branch -d feature-tea
```

```text
  feature-tea
* main
Deleted branch feature-tea (was bb67674).
```

`git branch --merged` lists branches whose commits are all contained in the current branch: safe to delete. The
commits stay: they are part of `main` now.

## Command breakdown

| Command | What it does |
|---|---|
| `git branch --merged` / `--no-merged` | branches whose work is / is not in the current branch |
| `git branch -d NAME` | delete if merged (safe) |
| `git branch -D NAME` | delete even if not merged (force) |
| `git push origin --delete NAME` | delete a branch on the remote (lesson 42) |

## Hands-on exercise

**Instructions.** List the branches that are **not** merged into `main`.

**Expected result.** `experiment`.

**Verification.**

<!-- test: contains=experiment -->
```bash
cd ~/git-practice/lesson-22
git branch --no-merged
```

## Break it

<!-- test: fail; contains=not fully merged; output -->
```bash
git branch -d experiment 2>&1
```

```text
error: the branch 'experiment' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D experiment'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
```

## Troubleshoot

`error: the branch 'experiment' is not fully merged`: `experiment` has a commit (`Try oat milk`) that no other branch
contains; deleting the label would leave that commit unreachable. Look at what would be lost:

<!-- test: contains=Try oat milk -->
```bash
git log --oneline main..experiment
```

## Fix

Decide. Either merge the work first, or confirm it is really unwanted and force the delete. Here the experiment is
abandoned, so force it, and note the commit ID first (lesson 79 shows how to get it back anyway):

<!-- test: contains=Deleted branch experiment; output -->
```bash
git rev-parse --short experiment
git branch -D experiment
```

```text
b6d8466
Deleted branch experiment (was b6d8466).
```

## Real-world example

After a pull request is merged, the feature branch is deleted (GitHub offers a button, or deletes it automatically if
the repository setting is on). Locally, `git fetch --prune` (lesson 40) removes the stale remote-tracking copies, and
`git branch --merged main` lists local branches safe to clean up.

## Practice challenge

Delete every local branch that is merged into `main`, except `main` itself, in one command line.

<details>
<summary>Solution</summary>

<!-- test: contains=main; output -->
```bash
cd ~/git-practice/lesson-22
git branch done-1 && git branch done-2
git branch --merged main | grep -vE '^\*|^\s*main$' | xargs -r git branch -d
git branch
```

```text
Deleted branch done-1 (was bb67674).
Deleted branch done-2 (was bb67674).
* main
```

Always run the list (`git branch --merged main`) alone first and read it before piping it into a delete.

</details>

## Recap

- `-d` deletes only merged branches; `-D` forces.
- Deleting a branch deletes a label; merged commits stay in history.
- Before `-D`, look at `git log main..BRANCH`: that is exactly what you are throwing away.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-22
```

Next: [Module 06 · Lesson 23 · What is a merge?](../../06-merging/23-what-is-merge/README.md).
