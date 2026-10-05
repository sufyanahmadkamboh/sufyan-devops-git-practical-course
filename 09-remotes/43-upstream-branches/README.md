# Lesson 43 · Upstream branches

> Level 8 · Remote repositories · ⏱ 15 minutes

## What are we learning?

The upstream (tracking) branch is the remote branch a local branch is connected to. It is what lets you type plain
`git push`, `git pull` and see "ahead 1, behind 2" in `git status`.

## Visual

```text
 local branch        upstream
 main          ───►  origin/main            set automatically by clone / git switch NAME
 feature-chai  ───►  origin/feature-chai    set with git push -u origin feature-chai

 git branch -vv:
   * feature-chai 1a2b3c4 [origin/feature-chai: ahead 1] Add chai
     main         4267004 [origin/main] Add prices
```

## Lab setup

<!-- test: contains=lesson-43 -->
```bash
bash scripts/new-lab.sh lesson-43 remote
cd ~/git-practice/lesson-43/ada
```

## Demonstration

<!-- test: contains=[origin/main]; output -->
```bash
git branch -vv
```

```text
* main 4267004 [origin/main] Add prices
```

A new branch has no upstream yet. Push it with `-u` to create the remote branch and connect it:

<!-- test: contains=set up to track 'origin/feature-chai'; output -->
```bash
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push -u origin feature-chai
git branch -vv
```

```text
To ~/git-practice/lesson-43/server/cafe.git
 * [new branch]      feature-chai -> feature-chai
branch 'feature-chai' set up to track 'origin/feature-chai'.
* feature-chai 6cb7a99 [origin/feature-chai] Add chai
  main         4267004 [origin/main] Add prices
```

Now plain `git push` / `git pull` work on it, and `git status` compares with it:

<!-- test: contains=ahead of 'origin/feature-chai' by 1 commit; output -->
```bash
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git status | head -2
```

```text
On branch feature-chai
Your branch is ahead of 'origin/feature-chai' by 1 commit.
```

## Command breakdown

| Command | What it does |
|---|---|
| `git branch -vv` | each branch with its upstream and ahead/behind |
| `git push -u origin BRANCH` | push and set the upstream |
| `git branch -u origin/BRANCH` | set the upstream of the current branch |
| `git branch --unset-upstream` | remove it |
| `@{u}` / `@{upstream}` | "my upstream" in any command: `git log @{u}..` |
| `git config --global push.autoSetupRemote true` | `git push` sets the upstream by itself the first time |

## Hands-on exercise

**Instructions.** Using `@{u}`, list the commits on `feature-chai` that are not pushed yet.

**Expected result.** `Price chai`.

**Verification.**

<!-- test: contains=Price chai -->
```bash
cd ~/git-practice/lesson-43/ada
git log --oneline '@{u}..'
```

## Break it

Create another branch and push it without `-u`:

<!-- test: fail; contains=has no upstream branch; output -->
```bash
git switch -q -c feature-mocha && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

```text
fatal: The current branch feature-mocha has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin feature-mocha

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```

## Troubleshoot

`fatal: The current branch feature-mocha has no upstream branch.`: Git does not know where to push this branch; it
does not assume a remote branch of the same name. The message prints the exact command to use.

## Fix

<!-- test: contains=origin/feature-mocha; output -->
```bash
git push -q -u origin feature-mocha
git branch -vv | grep feature-mocha
```

```text
* feature-mocha f2833c1 [origin/feature-mocha] Add mocha
```

To never see the error again: `git config --global push.autoSetupRemote true`.

## Real-world example

A wrong upstream causes real accidents: a branch created with `git switch -c fix origin/main` tracks
`origin/main`, so a plain `git push` with `push.default=upstream` would push your fix straight to `main`. With the default
`push.default=simple`, Git refuses because the names differ. `git branch -vv` shows the truth; `git branch -u` corrects
it (troubleshooting lab 11).

## Practice challenge

Create `hotfix` from `origin/main`, check its upstream, and change it to `origin/hotfix` after pushing.

<details>
<summary>Solution</summary>

<!-- test: contains=[origin/hotfix]; output -->
```bash
cd ~/git-practice/lesson-43/ada
git switch -q -c hotfix origin/main
git branch -vv | grep hotfix
git push -q -u origin hotfix
git branch -vv | grep hotfix
```

```text
* hotfix        4267004 [origin/main] Add prices
* hotfix        4267004 [origin/hotfix] Add prices
```

</details>

## Recap

- The upstream connects a local branch to a remote branch: plain push/pull and ahead/behind use it.
- `git push -u origin BRANCH` the first time (or `push.autoSetupRemote true`).
- Check with `git branch -vv`; fix with `git branch -u`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-43
```

Next: [Module 10 · Lesson 44 · What is GitHub?](../../10-github/44-what-is-github/README.md).
