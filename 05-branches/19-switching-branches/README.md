# Lesson 19 · Switching branches

> Level 4 · Branches · ⏱ 20 minutes

## What are we learning?

`git switch` moves `HEAD` to another branch and updates your files to match it. We also meet the older
`git checkout`, and what Git does with uncommitted changes when you switch.

## Visual

```text
 git switch feature-tea

 A ── B ── C        ← main
            ╲
             D      ← feature-tea (HEAD)        HEAD moved; the working directory now shows commit D
```

`git checkout` did this before Git 2.23, and also restored files, created branches and more. `git switch` (branches)
and `git restore` (files) split that job into two clear commands. Both still work; prefer the new ones.

## Lab setup

<!-- test: contains=lesson-19 -->
```bash
bash scripts/new-lab.sh lesson-19 diverged
cd ~/git-practice/lesson-19
```

## Demonstration

On `main`, the menu has three items:

<!-- test: contains=On branch main; output -->
```bash
git status | head -1
cat menu.txt
```

```text
On branch main
espresso
latte
cappuccino
```

<!-- test: contains=green tea; output -->
```bash
git switch feature-tea
cat menu.txt
cat .git/HEAD
```

```text
Switched to branch 'feature-tea'
espresso
latte
cappuccino
green tea
ref: refs/heads/feature-tea
```

The file changed on disk, and `HEAD` now names `feature-tea`. Back again:

<!-- test: contains=main; output -->
```bash
git switch main
cat menu.txt
git switch -                 # "-" = the previous branch, like cd -
git branch --show-current
git switch -q main
```

```text
Switched to branch 'main'
espresso
latte
cappuccino
Switched to branch 'feature-tea'
feature-tea
```

The older command does the same for branches:

<!-- test: contains=feature-tea -->
```bash
git checkout feature-tea 2>&1
git checkout main 2>&1
```

## Command breakdown

| Command | What it does |
|---|---|
| `git switch NAME` | move to branch NAME |
| `git switch -` | back to the previous branch |
| `git branch --show-current` | print the current branch |
| `git checkout NAME` | the older equivalent |
| `git switch --discard-changes NAME` | switch and throw away local changes (careful) |

## Hands-on exercise

**Instructions.** Make an uncommitted change to `prices.txt`, switch to `feature-tea`, and check whether the change
came with you.

**Expected result.** The change follows you: `prices.txt` is modified on `feature-tea` too, because that file is the
same in both branches, so Git can keep your edit.

<!-- test-run: cd ~/git-practice/lesson-19 && echo "chai 3.00" >> prices.txt && git switch -q feature-tea -->

**Verification.**

<!-- test: contains=M prices.txt -->
```bash
cd ~/git-practice/lesson-19
git branch --show-current
git status --short
```

## Break it

Now an uncommitted change to a file that **differs** between the branches:

<!-- test: fail; contains=would be overwritten by checkout; output -->
```bash
git restore prices.txt
echo "matcha" >> menu.txt
git switch main 2>&1
```

```text
error: Your local changes to the following files would be overwritten by checkout:
	menu.txt
Please commit your changes or stash them before you switch branches.
Aborting
```

## Troubleshoot

`Your local changes to the following files would be overwritten by checkout: menu.txt`. `menu.txt` is different on
`main`; switching would have to replace your edited version, so Git refuses rather than destroy your work. You are still
on `feature-tea`, nothing was lost:

<!-- test: contains=M menu.txt -->
```bash
git branch --show-current
git status --short
```

## Fix

Three options: commit the change, stash it (lesson 35), or discard it. Commit it here:

<!-- test: contains=main -->
```bash
git commit -q -am "Add matcha"
git switch main
git branch --show-current
```

## Real-world example

You are mid-change on a feature when a reviewer asks you to check something on `main`. `git switch main` refuses
because of your edits: that refusal is the safety net. Commit (a work-in-progress commit you will tidy up later),
stash, or use a second worktree (lesson 87) so both branches are checked out at once.

## Practice challenge

Use `git switch` to look at the code as it was on `feature-tea` without being able to commit to the branch by mistake.
(Hint: lesson 78, `--detach`.)

<details>
<summary>Solution</summary>

<!-- test: contains=HEAD detached; output -->
```bash
cd ~/git-practice/lesson-19
git switch --detach feature-tea 2>&1
git status | head -1
git switch -q main
```

```text
HEAD is now at f4fa504 Add matcha
HEAD detached at refs/heads/feature-tea
```

A detached `HEAD` points at a commit, not a branch: you can look around, and new commits would not move any branch.

</details>

## Recap

- `git switch NAME` moves `HEAD` and updates your files; `git switch -` goes back.
- Uncommitted changes come along when they don't conflict; otherwise Git refuses, to protect your work.
- `git checkout` still works; `git switch`/`git restore` are clearer.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-19
```

Next: [Lesson 20 · Create and switch in one command](../20-create-and-switch/README.md).
