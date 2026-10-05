# Lesson 08 · git status

> Level 2 · Repositories · ⏱ 20 minutes

## What are we learning?

How to read every part of `git status`: the branch line, the remote line, and the three sections of changes. It is
the command you will run more than any other.

## Visual

```text
On branch main                                      ← where you are (lesson 18)
Your branch is ahead of 'origin/main' by 1 commit.  ← compared with the remote (lesson 43), when there is one

Changes to be committed:                            ← STAGED: goes into the next commit (lesson 09)
        modified:   menu.txt

Changes not staged for commit:                      ← MODIFIED in the working directory, not staged
        modified:   prices.txt

Untracked files:                                    ← NEW files Git has never seen committed
        hours.txt
```

## Lab setup

<!-- test: contains=lesson-08 -->
```bash
bash scripts/new-lab.sh lesson-08 remote
cd ~/git-practice/lesson-08/ada
```

## Demonstration

A clone of a remote repository, untouched:

<!-- test: contains=up to date with 'origin/main'; output -->
```bash
git status
```

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Now one change of each kind, plus one local commit:

<!-- test: output -->
```bash
echo "green tea" >> menu.txt && git add menu.txt && git commit -q -m "Add green tea"
echo "chai" >> menu.txt && git add menu.txt          # staged
sed -i 's/latte 3.20/latte 3.30/' prices.txt         # modified, not staged
echo "Open 8-18" > hours.txt                         # untracked
git status
```

```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   menu.txt

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   prices.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	hours.txt
```

Read it top to bottom:

1. `On branch main`: the current branch.
2. `ahead of 'origin/main' by 1 commit`: one commit exists here and not yet on the remote (push it, lesson 42).
3. *Changes to be committed*: `menu.txt` has a staged change (`chai`).
4. *Changes not staged*: `prices.txt` was modified but not staged. `menu.txt` does not appear here, because
   everything changed in it is staged.
5. *Untracked files*: `hours.txt`.

The same in two letters per file:

<!-- test: contains=?? hours.txt; output -->
```bash
git status --short --branch
```

```text
## main...origin/main [ahead 1]
M  menu.txt
 M prices.txt
?? hours.txt
```

The first column is the staging area, the second the working directory: `M ` staged, ` M` modified not staged,
`MM` both, `??` untracked.

## Command breakdown

| Command | Use |
|---|---|
| `git status` | the full report, with hints for the next commands |
| `git status -s` / `--short` | compact, two columns |
| `git status -sb` | compact plus the branch and ahead/behind line |
| `git status --ignored` | also list ignored files (lesson 73) |

## Hands-on exercise

**Instructions.** Make `menu.txt` appear with `MM`: staged changes **and** further unstaged changes in the same file.

**Expected result.** `git status --short` shows `MM menu.txt`.

<!-- test-run: cd ~/git-practice/lesson-08/ada && echo "matcha" >> menu.txt -->

**Verification.**

<!-- test: contains=MM menu.txt -->
```bash
cd ~/git-practice/lesson-08/ada
git status --short
```

## Break it

Read `git status` wrongly and lose work: you think `prices.txt` is staged, commit, and push, but the latte price change
was not in the commit.

<!-- test: contains=prices.txt -->
```bash
git commit -q -m "Add chai"
git status --short
```

## Troubleshoot

After the commit, `git status` still lists ` M prices.txt` (and the extra `matcha` line in `menu.txt`): those changes
were **not staged**, so they were not committed. The commit contains only what was in *Changes to be committed*:

<!-- test: contains=chai; absent=latte; output -->
```bash
git show --stat --format='%s' HEAD
git show HEAD | grep '^[+-][^+-]'
```

```text
Add chai

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
+chai
```

## Fix

Stage the missing change and commit it (or, if the commit is not pushed yet, add it to the last commit with
`git commit --amend`, lesson 11):

<!-- test: contains=nothing to commit -->
```bash
git add prices.txt menu.txt && git commit -q -m "Raise the latte price, add matcha"
rm hours.txt
git status
```

## Real-world example

Before every commit, run `git status` (or `git status -sb`) and read all three sections. Before every push, the
`ahead/behind` line tells you whether a teammate pushed meanwhile. Most "I committed the wrong thing" incidents start
with skipping this one command.

## Practice challenge

Create a state where `git status --short` shows `A ` (a new file staged), ` D` (a deleted tracked file, not staged)
and `??` (an untracked file) at the same time.

<details>
<summary>Solution</summary>

<!-- test: contains=A  specials.txt; contains= D README.md; contains=?? notes.txt; output -->
```bash
cd ~/git-practice/lesson-08/ada
echo "2 for 1" > specials.txt && git add specials.txt
rm README.md
echo "todo" > notes.txt
git status --short
```

```text
 D README.md
A  specials.txt
?? notes.txt
```

</details>

## Recap

- `git status`: branch, ahead/behind, then staged / not staged / untracked.
- Only *Changes to be committed* goes into the next commit.
- `git status -sb`: two columns (staging area, working directory) plus the branch line.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-08
```

Next: [Module 03 · Lesson 09 · git add](../../03-commits/09-git-add/README.md).
