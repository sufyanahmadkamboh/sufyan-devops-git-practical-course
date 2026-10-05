# Lesson 51 · What is a pull request?

> Level 11 · Pull requests · ⏱ 15 minutes

## What are we learning?

A pull request (PR) is a request to merge one branch into another, wrapped in a page for discussion: the commits, the
diff, a merge check, reviews and automated checks. Underneath it is plain Git, which we reproduce locally first.

## Visual

```text
 feature branch (pushed)
        │
        ▼
 Pull Request  "Add green tea"   base: main  ←  compare: feature-tea
        │      ├── Commits tab        git log main..feature-tea
        │      ├── Files changed tab  git diff main...feature-tea
        │      └── "No conflicts"     git merge-tree main feature-tea
        ▼
 Review   (lesson 53: comments, suggestions, approve / request changes)
        ▼
 Checks   (CI: tests, lint, build; lesson 98)
        ▼
 Merge    (lesson 54: merge commit, squash or rebase)
```

## Lab setup

Two labs: `lesson-51` for the demonstration, `lesson-51b` (with a conflict) for "Break it".

<!-- test: contains=lesson-51b -->
```bash
bash scripts/new-lab.sh lesson-51b conflict
bash scripts/new-lab.sh lesson-51 diverged
cd ~/git-practice/lesson-51
git log --oneline --graph --all
```

## Demonstration

What a PR from `feature-tea` into `main` would show, computed locally.

**Commits** tab: commits on the branch that are not on the base:

<!-- test: contains=Add green tea to the menu; output -->
```bash
git log --oneline main..feature-tea
```

```text
bb67674 (feature-tea) Add green tea to the menu
```

**Files changed** tab: the three-dot diff, i.e. the branch's changes since it left `main` (main's own new commit,
"Add opening hours", is not part of the PR):

<!-- test: contains=+green tea; absent=Open every day; output -->
```bash
git diff main...feature-tea
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

**Merge check** ("This branch has no conflicts with the base branch"): a merge computed without touching any files:

<!-- test: output -->
```bash
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts: can be merged automatically"
```

```text
no conflicts: can be merged automatically
```

## Command breakdown

| PR page | Git equivalent |
|---|---|
| Commits | `git log BASE..HEAD-BRANCH` |
| Files changed | `git diff BASE...HEAD-BRANCH` (three dots) |
| "No conflicts" / "conflicts must be resolved" | `git merge-tree --write-tree BASE BRANCH` (exit status 0 / 1) |
| Merge button | `git merge` (or squash / rebase, lesson 54) executed by GitHub |

## Hands-on exercise

**Instructions.** Show only the **names** of the files the PR would change.

**Expected result.** `menu.txt`.

**Verification.**

<!-- test: contains=menu.txt; absent=README -->
```bash
cd ~/git-practice/lesson-51
git diff --name-only main...feature-tea
```

## Break it

A branch that conflicts with its base, like a PR GitHub marks "This branch has conflicts that must be resolved":

<!-- test: fail; contains=CONFLICT (content); output -->
```bash
cd ~/git-practice/lesson-51b
git merge-tree --write-tree --name-only main feature-tea
```

```text
c1ec90e49d06aa38520744c366604c4ec932383a
prices.txt

Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
```

## Troubleshoot

Exit status 1 and `CONFLICT (content): Merge conflict in prices.txt`: both branches changed the same line. GitHub
cannot merge the PR; the author has to update the branch.

## Fix

The PR author brings `main` into the branch and resolves the conflict there (lesson 27), then pushes; the PR updates
itself:

<!-- test: contains=no conflicts; output -->
```bash
git switch -q feature-tea
git merge main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q -m "Merge main into feature-tea"
git merge-tree --write-tree main feature-tea > /dev/null && echo "no conflicts: can be merged automatically"
```

```text
no conflicts: can be merged automatically
```

## Real-world example

A PR is the unit of change in most teams: one focused purpose ("Bump the chart to 1.4.0"), a description of why and
how it was tested, a link to the issue, small enough to review in 15 minutes. Branch protection (lesson 59) then makes
the PR the only way into `main`: no direct pushes, required review, required green checks.

## Practice challenge

How many commits ahead of and behind `main` is `feature-tea` in the first lab (GitHub shows this as "N commits ahead,
M commits behind main")?

<details>
<summary>Solution</summary>

<!-- test: output -->
```bash
cd ~/git-practice/lesson-51
git rev-list --left-right --count main...feature-tea | awk '{print "behind", $1, "ahead", $2}'
```

```text
behind 1 ahead 1
```

</details>

## Recap

- A PR = a branch comparison + discussion + checks + a merge button.
- Commits tab = `base..branch`; Files changed = `base...branch`; conflicts = `git merge-tree`.
- Conflicts are fixed on the branch by its author; the PR updates automatically when the branch is pushed.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-51 ~/git-practice/lesson-51b
```

Next: [Lesson 52 · Creating a pull request](../52-create-pull-request/README.md).
