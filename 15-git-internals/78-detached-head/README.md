# Lesson 78 · Detached HEAD

> Level 15 · Git internals · ⏱ 20 minutes

## What are we learning?

"Detached HEAD" means `HEAD` points directly to a commit instead of to a branch. It happens when you check out a tag,
a commit ID or a remote branch. Looking around is perfectly fine; commits made there belong to no branch and are easy
to lose. We create the situation on purpose and recover safely.

## Visual

```text
 attached:   HEAD → main → C            detached:   HEAD → B   (no branch in between)

 A ── B ── C   ← main                   commit while detached:   A ── B ── C   ← main
      ▲                                                                ╲
     HEAD                                                               X   ← HEAD only
                                         switch away → X is referenced by nothing (reflog only)
```

## Lab setup

<!-- test: contains=lesson-78 -->
```bash
bash scripts/new-lab.sh lesson-78 history
cd ~/git-practice/lesson-78
git tag v1.0.0 4267004
```

## Demonstration

<!-- test: contains=HEAD is now at 4267004; output -->
```bash
git switch --detach v1.0.0
```

```text
HEAD is now at 4267004 Add prices
```

<!-- test: contains=HEAD detached at v1.0.0; output -->
```bash
git status | head -2
cat .git/HEAD
git branch
```

```text
HEAD detached at v1.0.0
nothing to commit, working tree clean
4267004871ae95e12690719f02460f9e3c935cf5
* (HEAD detached at v1.0.0)
  main
```

`.git/HEAD` contains a commit ID, not `ref: refs/heads/...`. Inspecting old code, running old tests, building an old
release: all fine here.

## Command breakdown

| Command | Effect |
|---|---|
| `git switch --detach REV` | detach on purpose |
| `git checkout TAG / SHA` | detaches too (with a warning) |
| `git switch -c NAME` | create a branch here: no longer detached |
| `git switch BRANCH` / `git switch -` | go back to a branch |
| `git branch NAME SHA` | rescue a commit after leaving it |

## Hands-on exercise

**Instructions.** While detached at `v1.0.0`, check whether `menu.txt` already had mocha in that release.

**Expected result.** No mocha.

**Verification.**

<!-- test: absent=mocha -->
```bash
cd ~/git-practice/lesson-78
cat menu.txt
```

## Break it

Make a hotfix commit while detached, then switch back to `main`:

<!-- test: contains=Warning: you are leaving 1 commit behind; output -->
```bash
sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix: espresso price"
git switch main 2>&1
```

```text
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  706d7af Hotfix: espresso price

If you want to keep it by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> 706d7af

Switched to branch 'main'
```

## Troubleshoot

Git warns: the commit is not connected to any branch, so no branch log shows it and garbage collection will eventually
delete it. The warning even prints the command to keep it. If the terminal output is gone, the reflog still has it:

<!-- test: contains=Hotfix: espresso price; output -->
```bash
git reflog | grep -m1 "Hotfix"
```

```text
706d7af HEAD@{1}: commit: Hotfix: espresso price
```

## Fix

<!-- test: contains=Hotfix: espresso price; output -->
```bash
git branch hotfix-espresso "$(git reflog --format=%h --grep-reflog='commit: Hotfix' | head -1)"
git log --oneline -1 hotfix-espresso
```

```text
706d7af (hotfix-espresso) Hotfix: espresso price
```

## Real-world example

CI systems often check out the exact commit being built: a detached HEAD by design (GitHub Actions on a pull request,
Jenkins with a SHA). A release script that commits a version bump there and pushes "the branch" fails or pushes
nothing. Such scripts must create or check out a branch first (`git switch -c release-bump`), or push
`HEAD:refs/heads/main` explicitly.

## Practice challenge

Detach at `HEAD~2`, make a commit, and **before** leaving, turn it into a branch with one command.

<details>
<summary>Solution</summary>

<!-- test: contains=On branch experiment; output -->
```bash
cd ~/git-practice/lesson-78
git switch -q --detach HEAD~2
echo "idea" > idea.txt && git add idea.txt && git commit -q -m "Try an idea"
git switch -c experiment
git status | head -1
```

```text
Switched to a new branch 'experiment'
On branch experiment
```

</details>

## Recap

- Detached HEAD = HEAD points at a commit, not a branch; normal when inspecting tags or CI checkouts.
- Commits made while detached belong to no branch: `git switch -c NAME` before leaving.
- Lost one anyway? `git reflog` + `git branch NAME SHA`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-78
```

Next: [Module 16 · Lesson 79 · Recover a deleted branch](../../16-recovery/79-recover-deleted-branch/README.md).
