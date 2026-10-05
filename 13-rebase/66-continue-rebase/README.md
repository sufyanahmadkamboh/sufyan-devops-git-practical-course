# Lesson 66 · Continuing a rebase

> Level 13 · Rebase · ⏱ 20 minutes

## What are we learning?

`git rebase --continue` resumes a paused rebase. A rebase pauses for two reasons: a conflict (lesson 64) or an `edit`
stop you asked for. We use `edit` to change an old commit in the middle of the history, and the next commits follow
automatically.

## Visual

```text
 git rebase -i HEAD~4  with  edit 269869e Price green tea
   replay "Add green tea"   ✓
   replay "Price green tea" ✓ → STOP (edit): change files, git commit --amend
   git rebase --continue
   replay "Add mocha"       ✓
   replay "Price mocha"     ✓ → done
```

## Lab setup

<!-- test: contains=lesson-66 -->
```bash
bash scripts/new-lab.sh lesson-66 history
cd ~/git-practice/lesson-66
git log --oneline -4
```

## Demonstration

The commit "Price green tea" should also have announced the new tea in the README. Stop at that commit:

<!-- test: contains=Stopped at; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/edit/'" git rebase -i HEAD~4 2>&1
git status | head -4
```

```text
Rebasing (2/4)
Stopped at 269869e...  # Price green tea
You can amend the commit now, with

  git commit --amend 

Once you are satisfied with your changes, run

  git rebase --continue
interactive rebase in progress; onto 4267004
Last commands done (2 commands done):
   pick 6833580 # Add green tea
   edit 269869e # Price green tea
```

The working directory is the snapshot of "Price green tea". Change it and **amend** the commit:

<!-- test: contains=README.md -->
```bash
echo "Now serving green tea." >> README.md
git commit -q --amend --no-edit -a
git show --stat --format=%s HEAD | tail -3
```

Continue: the later commits are replayed on top of the changed one.

<!-- test: contains=Successfully rebased; output -->
```bash
git rebase --continue
git log --oneline -4
git log --oneline -1 -- README.md
```

```text
Rebasing (3/4)
Rebasing (4/4)
Successfully rebased and updated refs/heads/main.
0162fb1 (HEAD -> main) Price mocha
c87cd51 Add mocha
efa9046 Price green tea
6833580 Add green tea
efa9046 Price green tea
```

## Command breakdown

| Command | When |
|---|---|
| `git rebase --continue` | after resolving a conflict (`git add`) or after amending at an `edit` stop |
| `git commit --amend` | at an `edit` stop: change the stopped commit |
| `git rebase --skip` | drop the current commit |
| `git rebase --edit-todo` | change the remaining to-do list mid-rebase |
| `git reset HEAD~1` at an `edit` stop | split the commit: then several `git add`/`git commit`, then continue |

## Hands-on exercise

**Instructions.** Stop at "Add green tea" with `edit`, add a **new** commit after it (a notes file), and continue.

**Expected result.** A new commit "Add tea notes" right after "Add green tea".

<!-- test-run: cd ~/git-practice/lesson-66 && GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~4 && echo "green tea: sencha" > notes.txt && git add notes.txt && git commit -q -m "Add tea notes" && git rebase --continue > /dev/null -->

**Verification.**

<!-- test: contains=Add tea notes -->
```bash
cd ~/git-practice/lesson-66
git log --oneline -6 --reverse
```

## Break it

At an `edit` stop meant to **change** "Add mocha", commit without `--amend` (a very common slip), and continue:

<!-- test: contains=Mark mocha as seasonal; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~2
sed -i 's/^mocha$/mocha (seasonal)/' menu.txt
git commit -q -am "Mark mocha as seasonal"
git rebase --continue
git log --oneline -3
```

```text
Stopped at 705a714...  # Add mocha
You can amend the commit now, with

  git commit --amend 

Once you are satisfied with your changes, run

  git rebase --continue
a83ed5c (HEAD -> main) Price mocha
585d1aa Mark mocha as seasonal
705a714 Add mocha
```

## Troubleshoot

No error: Git simply kept your extra commit. The history now has "Add mocha" **and** "Mark mocha as seasonal", instead
of one corrected "Add mocha". At an `edit` stop, `git commit` adds a commit; `git commit --amend` changes the stopped
one. Both are valid, so Git cannot warn you.

## Fix

Fold the extra commit into "Add mocha" with a second interactive rebase (`fixup` keeps the first message):

<!-- test: absent=Mark mocha as seasonal; contains=mocha (seasonal); output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/fixup/'" git rebase -q -i HEAD~3
git log --oneline -3
git show HEAD~1 | grep "^+mocha"
```

```text
881b387 (HEAD -> main) Price mocha
e49b0d2 Add mocha
33f0085 Price green tea
+mocha (seasonal)
```

## Real-world example

Interactive rebase with `edit` is how you fix a commit deep in your branch: remove an accidentally committed debug
file from commit 3 of 8, correct a migration in commit 5, add a forgotten test to the commit that introduced the
feature. Every later commit is replayed automatically; you only pay attention where Git stops.

## Practice challenge

Mid-rebase, change your mind about the remaining steps: start an interactive rebase with `edit` on the first commit,
then use `--edit-todo` to drop "Price mocha" before continuing.

<details>
<summary>Solution</summary>

<!-- test: absent=Price mocha; output -->
```bash
cd ~/git-practice/lesson-66
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~3
GIT_EDITOR="sed -i '/Price mocha/s/^pick/drop/'" git rebase --edit-todo
git rebase --continue > /dev/null
git log --oneline -3
```

```text
Stopped at 33f0085...  # Price green tea
You can amend the commit now, with

  git commit --amend 

Once you are satisfied with your changes, run

  git rebase --continue
e49b0d2 (HEAD -> main) Add mocha
33f0085 Price green tea
49037db Add tea notes
```

</details>

## Recap

- A rebase pauses on conflicts and `edit` stops; `git rebase --continue` resumes.
- At an `edit` stop: `--amend` changes the commit, a plain commit adds one.
- Fix a slip with another interactive rebase (`fixup`).

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-66
```

Next: [Module 14 · Lesson 67 · Cherry-pick](../../14-advanced-git/67-cherry-pick/README.md).
