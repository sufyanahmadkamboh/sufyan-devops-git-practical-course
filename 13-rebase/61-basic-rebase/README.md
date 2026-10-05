# Lesson 61 · Basic rebase

> Level 13 · Rebase · ⏱ 20 minutes

## What are we learning?

The everyday rebase: bring your feature branch up to date with `main` before opening or updating a PR, and
`git pull --rebase` to keep your local commits on top of your teammates' work.

## Visual

```text
 git switch feature && git rebase main          git pull --rebase (on main)

 main     A ── B ── D                           origin/main  A ── B ── G      (Grace pushed G)
                     ╲                          main         A ── B ── X      (your local X)
 feature              C1' ── C2'                    after:   A ── B ── G ── X'   (no merge commit)
```

## Lab setup

<!-- test: contains=lesson-61 -->
```bash
bash scripts/new-lab.sh lesson-61 diverged
cd ~/git-practice/lesson-61
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git log --oneline --graph --all
```

## Demonstration

Update the feature branch with `main`'s latest commit:

<!-- test: contains=Successfully rebased; output -->
```bash
git rebase main
git log --oneline --graph --all
```

```text
Rebasing (1/2)
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
* 83a2606 (HEAD -> feature-tea) Price green tea
* d9dd76d Add green tea to the menu
* f40d080 (main) Add opening hours
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

Both feature commits are now on top of "Add opening hours". `main` can take them with a fast-forward:

<!-- test: contains=Fast-forward -->
```bash
git switch -q main && git merge --ff-only feature-tea
```

## Command breakdown

| Command | When |
|---|---|
| `git rebase main` | update your feature branch with main (local main must be current) |
| `git fetch && git rebase origin/main` | the same against the server's main, without updating local main |
| `git pull --rebase` | update a branch from its upstream, local commits on top |
| `git rebase --autostash main` | stash uncommitted changes first, re-apply after |
| `git config --global pull.rebase true` | make `git pull` rebase by default |

## Hands-on exercise

**Instructions.** Create `feature-chai` from the commit **before** the last two, add a commit, and rebase it onto `main`.

**Expected result.** `feature-chai`'s commit sits on top of `main`.

<!-- test-run: cd ~/git-practice/lesson-61 && git switch -q -c feature-chai HEAD~2 && echo chai >> notes.txt && git add notes.txt && git commit -q -m "Add chai notes" && git rebase -q main -->

**Verification.**

<!-- test: contains=0 -->
```bash
cd ~/git-practice/lesson-61
git rev-list --count feature-chai..main
git log --oneline -2 feature-chai
```

## Break it

Rebase with uncommitted changes in your folder:

<!-- test: fail; contains=cannot rebase: You have unstaged changes; output -->
```bash
git switch -q main && git switch -q -c feature-mocha HEAD~3
echo "mocha" > specials.txt && git add specials.txt && git commit -q -m "Add mocha special"
sed -i 's/espresso 2.50/espresso 2.55/' prices.txt
git rebase main 2>&1
```

```text
error: cannot rebase: You have unstaged changes.
error: Please commit or stash them.
```

## Troubleshoot

`cannot rebase: You have unstaged changes.`: rebase rewrites the working directory commit by commit; it refuses to
risk your uncommitted work. `git status` shows the draft change in `prices.txt`.

## Fix

Let Git stash and restore it around the rebase:

<!-- test: contains=Applied autostash; output -->
```bash
git rebase --autostash main 2>&1 | grep -v "^hint:" || true
git status --short
```

```text
Created autostash: 8928ff6
Rebasing (1/1)
Applied autostash.
Successfully rebased and updated refs/heads/feature-mocha.
 M prices.txt
```

The draft (`M prices.txt`) is back, on top of the rebased branch.

## Real-world example

`git config --global pull.rebase true` plus `rebase.autoStash true` is a common developer setup: `git pull` on a
branch with local commits never creates "Merge branch 'main' of github.com:..." noise, and uncommitted work is
carried along automatically.

## Practice challenge

From `main`, rebase `feature-mocha` onto `main` in one command, and list the commits it has that `main` does not.

<details>
<summary>Solution</summary>

<!-- test: contains=Add mocha special; output -->
```bash
cd ~/git-practice/lesson-61
git stash -q && git switch -q main
git rebase main feature-mocha
git branch --show-current
git log --oneline main..feature-mocha
git stash pop -q
```

```text
Current branch feature-mocha is up to date.
feature-mocha
6f33f8c (HEAD -> feature-mocha) Add mocha special
```

`git rebase BASE BRANCH` checks BRANCH out first; it is left checked out afterwards.

</details>

## Recap

- `git rebase main` puts your branch's commits on top of main: linear, fast-forwardable.
- `git pull --rebase` does the same against the upstream.
- Commit or `--autostash` uncommitted work before rebasing.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-61
```

Next: [Lesson 62 · Rebase vs merge](../62-rebase-vs-merge/README.md).
