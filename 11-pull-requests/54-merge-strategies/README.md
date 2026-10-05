# Lesson 54 · Merge strategies

> Level 11 · Pull requests · ⏱ 25 minutes

## What are we learning?

GitHub's merge button has three modes: **Create a merge commit**, **Squash and merge**, **Rebase and merge**. Each
leaves a different history on `main`. We reproduce all three locally to see the graphs, then merge a real PR.

## Visual

```text
 PR branch:   main: A ── B          feature: B ── f1 ── f2

 merge commit     A ── B ─────── M        all commits kept + a merge commit (the PR is visible as a bubble)
                        ╲       ╱
                         f1 ── f2
 squash and merge A ── B ── S             ONE new commit S = f1 + f2 (branch commits not on main)
 rebase and merge A ── B ── f1' ── f2'    commits replayed one by one, new IDs, no merge commit
```

## Lab setup

For the practice challenge, a clone of your GitHub practice repository (lesson 45):

<!-- test: github; contains=lesson-54-gh -->
```bash
bash scripts/new-lab.sh lesson-54-gh github
```

For the demonstration, three identical copies of a branch with two commits, one per strategy:

<!-- test: contains=lesson-54 -->
```bash
bash scripts/new-lab.sh lesson-54 diverged
cd ~/git-practice/lesson-54
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git switch -q main
for s in merge squash rebase; do git branch "main-$s" main; git branch "pr-$s" feature-tea; done
git log --oneline --graph --all | head -8
```

## Demonstration

**Create a merge commit** (GitHub always uses `--no-ff` here):

<!-- test: contains=Merge pull request; output -->
```bash
git switch -q main-merge
git merge -q --no-ff -m "Merge pull request #1 from pr-merge" pr-merge
git log --oneline --graph -5
```

```text
*   ec8ec87 (HEAD -> main-merge) Merge pull request #1 from pr-merge
|\  
| * ad7347d (pr-squash, pr-rebase, pr-merge, feature-tea) Price green tea
| * bb67674 Add green tea to the menu
* | f40d080 (main-squash, main-rebase, main) Add opening hours
|/  
* 4267004 Add prices
```

**Squash and merge**: the branch's changes become one new commit on `main`:

<!-- test: contains=Green tea (#2); output -->
```bash
git switch -q main-squash
git merge -q --squash pr-squash
git commit -q -m "Green tea (#2)"
git log --oneline --graph -3
git show --stat --format=%s HEAD
```

```text
Automatic merge went well; stopped before committing as requested
Squash commit -- not updating HEAD
* a42fe0f (HEAD -> main-squash) Green tea (#2)
* f40d080 (main-rebase, main) Add opening hours
* 4267004 Add prices
Green tea (#2)

 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
```

**Rebase and merge**: the commits replayed on top of `main`, without a merge commit:

<!-- test: contains=Price green tea; output -->
```bash
git switch -q pr-rebase
git rebase -q main-rebase
git switch -q main-rebase
git merge -q --ff-only pr-rebase
git log --oneline --graph -4
```

```text
* 36bc0cf (HEAD -> main-rebase, pr-rebase) Price green tea
* 247a7ac Add green tea to the menu
* f40d080 (main) Add opening hours
* 4267004 Add prices
```

Same files on all three, different histories:

<!-- test: output -->
```bash
for s in merge squash rebase; do echo "$s: $(git rev-parse "main-$s^{tree}" | cut -c1-7)  $(git rev-list --count "main-$s") commits"; done
```

```text
merge: ac2c891  7 commits
squash: ac2c891  5 commits
rebase: ac2c891  6 commits
```

## Command breakdown

| GitHub button | Local equivalent | History on main | Use when |
|---|---|---|---|
| Create a merge commit | `git merge --no-ff BRANCH` | all commits + merge commit | commits are meaningful; you want the PR boundary |
| Squash and merge | `git merge --squash BRANCH && git commit` | one commit per PR | messy branch history; one PR = one change |
| Rebase and merge | `git rebase main` + fast-forward | all commits, linear | clean, meaningful commits; linear history |
| `gh pr merge N --merge / --squash / --rebase` | | | CLI |

## Hands-on exercise

**Instructions.** On `main-squash`, find which PR branch commits are **not** on `main-squash` according to Git.

**Expected result.** Both `pr-squash` commits: squashing created a new commit, so Git does not consider them merged.

**Verification.**

<!-- test: contains=Price green tea; contains=Add green tea -->
```bash
cd ~/git-practice/lesson-54
git log --oneline main-squash..pr-squash
```

## Break it

After a squash merge, delete the PR branch locally the safe way:

<!-- test: fail; contains=not fully merged; output -->
```bash
git switch -q main-squash
git branch -d pr-squash 2>&1
```

```text
error: the branch 'pr-squash' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D pr-squash'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
```

## Troubleshoot

`error: the branch 'pr-squash' is not fully merged`: Git checks whether the branch's **commits** are reachable from
the current branch. After a squash they are not (the content is, inside a different commit). Check the content
instead:

<!-- test: contains=identical content -->
```bash
git diff --quiet main-squash pr-squash -- menu.txt prices.txt && echo "identical content: the work is on main-squash"
```

## Fix

Content verified: delete with `-D`. On GitHub, enable "Automatically delete head branches" so merged PR branches are
deleted for you.

<!-- test: contains=Deleted branch pr-squash -->
```bash
git branch -D pr-squash
```

## Real-world example

Many teams allow only **squash merging** on application repositories ("one PR = one commit on main", easy reverts,
the PR number in every commit subject) and keep **merge commits** for long-lived integration branches. Whatever is
chosen, configure it in Settings → General → Pull Requests so nobody has to remember.

## Practice challenge

Merge a real PR on your practice repository with **squash**, deleting its branch, and show the resulting commit on
GitHub's `main`.

<details>
<summary>Solution</summary>

<!-- test-run github: gh auth setup-git -->

<!-- test: github; contains=(#; output -->
```bash
cd ~/git-practice/lesson-54-gh
git push -q origin --delete chai 2> /dev/null || true
git switch -q -c chai
echo "chai" >> menu.txt && git commit -q -am "Add chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git push -q -u origin chai 2> /dev/null
gh pr create --base main --title "Add chai" --body "Chai on the menu, with its price." > /dev/null
gh pr merge chai --squash --delete-branch > /dev/null 2>&1
git switch -q main && git pull -q
git log --oneline -1
```

```text
0703734 (HEAD -> main, origin/main, origin/HEAD) Add chai (#11)
```

GitHub's squash commit subject is the PR title with the PR number: `Add chai (#N)`.

</details>

## Recap

- Merge commit: keeps everything + the PR boundary; squash: one commit per PR; rebase: linear, all commits.
- After squash/rebase merges, `git branch -d` says "not fully merged": compare content, then `-D`.
- Configure the allowed strategies per repository.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-54 ~/git-practice/lesson-54-gh
```

Next: [Module 12 · Lesson 55 · Team Git workflow](../../12-collaboration/55-team-workflow/README.md).
