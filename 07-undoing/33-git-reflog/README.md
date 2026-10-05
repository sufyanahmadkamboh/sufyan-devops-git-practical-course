# Lesson 33 · git reflog

> Level 6 · Undoing changes · ⏱ 20 minutes

## What are we learning?

The reflog is your local diary of every position `HEAD` and each branch have had: commits, resets, checkouts, merges,
rebases. Almost anything you "lost" with Git is still in it.

## Visual

```text
 git log      = the history of commits reachable from the branch     (what the project looks like)
 git reflog   = the history of where HEAD has been, in this clone      (what YOU did)

 HEAD@{0}  reset: moving to HEAD~3            ← now
 HEAD@{1}  commit: Price mocha                ← "before my mistake": still here!
 HEAD@{2}  commit: Add mocha
 ...
 entries expire after 90 days (30 for unreachable commits); the reflog is never pushed.
```

## Lab setup

<!-- test: contains=lesson-33 -->
```bash
bash scripts/new-lab.sh lesson-33 history
cd ~/git-practice/lesson-33
```

## Demonstration

A bad hard reset: three commits disappear from `main`:

<!-- test: contains=d6df412; output -->
```bash
git reset -q --hard HEAD~3
git log --oneline
```

```text
6833580 (HEAD -> main) Add green tea
4267004 Add prices
fc345e6 Add the menu
d6df412 Add README
```

`git log` shows only what is reachable now. The reflog shows what happened:

<!-- test: contains=reset: moving to HEAD~3; output -->
```bash
git reflog
```

```text
6833580 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
ecff18a HEAD@{1}: commit: Price mocha
2c389c0 HEAD@{2}: commit: Add mocha
269869e HEAD@{3}: commit: Price green tea
6833580 (HEAD -> main) HEAD@{4}: commit: Add green tea
4267004 HEAD@{5}: commit: Add prices
fc345e6 HEAD@{6}: commit: Add the menu
d6df412 HEAD@{7}: commit (initial): Add README
```

`HEAD@{1}` is the position just before the reset. Go back:

<!-- test: contains=Price mocha; output -->
```bash
git reset --hard 'HEAD@{1}'
git log --oneline -2
```

```text
HEAD is now at ecff18a Price mocha
ecff18a (HEAD -> main) Price mocha
2c389c0 Add mocha
```

## Command breakdown

| Command | What it shows / does |
|---|---|
| `git reflog` | where HEAD has been (`git reflog show HEAD`) |
| `git reflog show main` | where the branch `main` has been |
| `git log -g --oneline` | the reflog as a log |
| `HEAD@{2}` | HEAD two moves ago |
| `main@{yesterday}`, `main@{1.hour.ago}` | where main was at a time |
| `git reset --hard HEAD@{N}` | move back to that position |
| `git branch NAME HEAD@{N}` | rescue that position into a new branch (safer) |

## Hands-on exercise

**Instructions.** Using the reflog of the branch `main` (not of HEAD), find the commit `main` pointed to before the
reset, and create a branch `rescue` there.

**Expected result.** `rescue` points to "Price mocha".

<!-- test-run: cd ~/git-practice/lesson-33 && git branch rescue 'main@{2}' -->

**Verification.**

<!-- test: contains=Price mocha -->
```bash
cd ~/git-practice/lesson-33
git reflog show main | head -3
git log --oneline -1 rescue
```

## Break it

Delete a branch with unmerged work, a different way of "losing" commits:

<!-- test: contains=Deleted branch; output -->
```bash
git switch -q -c risky && echo "seasonal: pumpkin latte" >> menu.txt && git commit -q -am "Add pumpkin latte"
git switch -q main
git branch -D risky
```

```text
Deleted branch risky (was 4e57b0c).
```

## Troubleshoot

`Deleted branch risky (was ...)`: Git even printed the commit ID. If the terminal output is gone, the reflog still
has the commit, as the last position of HEAD on that branch:

<!-- test: contains=commit: Add pumpkin latte; output -->
```bash
git reflog | grep -m1 "pumpkin"
```

```text
4e57b0c HEAD@{1}: commit: Add pumpkin latte
```

## Fix

<!-- test: contains=Add pumpkin latte; output -->
```bash
lost=$(git reflog --format=%h --grep-reflog="commit: Add pumpkin latte" | head -1)
git branch risky "$lost"
git log --oneline -1 risky
```

```text
4e57b0c (risky) Add pumpkin latte
```

## Real-world example

A rebase went wrong, a force push from a colleague replaced your commits on a shared branch, an `--amend` swallowed
something: in every case your clone's reflog still has the earlier positions. `git reflog` → find the line from before
the mistake → `git branch rescue HEAD@{N}` → compare and recover. Lessons 79–81 practise these recoveries.

## Practice challenge

List the last positions of `main` with their times instead of `@{N}` numbers.

<details>
<summary>Solution</summary>

<!-- test: contains=main@{; output -->
```bash
cd ~/git-practice/lesson-33
git reflog show --date=relative main | head -3 | sed -E 's/[0-9]+ (seconds?|minutes?) ago/N seconds ago/'
```

```text
ecff18a (HEAD -> main, rescue) main@{N seconds ago}: reset: moving to HEAD@{1}
6833580 main@{N seconds ago}: reset: moving to HEAD~3
ecff18a (HEAD -> main, rescue) main@{9 months ago}: commit: Price mocha
```

`--date=relative` replaces `@{N}` with times (the `sed` only keeps the output stable here). `git show main@{10.minutes.ago}`
uses such times directly.

</details>

## Recap

- The reflog records every move of HEAD and branches in your clone.
- `HEAD@{N}` / `branch@{N}` name those old positions; reset or branch to them.
- It is local and expires (90 days by default): recover soon, and it never replaces pushing or backups.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-33
```

Next: [Module 08 · Lesson 34 · What is a stash?](../../08-stash/34-what-is-stash/README.md).
