# Lesson 64 · Rebase conflicts

> Level 13 · Rebase · ⏱ 25 minutes

## What are we learning?

A rebase replays commits one at a time, so a conflict can happen at each step. We create one on purpose and resolve it
step by step: read the status, fix the file, `git add`, `git rebase --continue`.

## Visual

```text
 git rebase main
   replay C1 ✓
   replay C2 ✗ CONFLICT  ── rebase pauses ──►  fix the file → git add FILE → git rebase --continue
   replay C3 ✓                                   (or git rebase --skip: drop C2 · git rebase --abort: undo all)

 note: during a rebase, "ours" = the branch you are rebasing ONTO (main), "theirs" = your commit being replayed.
       (the opposite of a merge on your branch)
```

## Lab setup

<!-- test: contains=lesson-64 -->
```bash
bash scripts/new-lab.sh lesson-64 conflict
cd ~/git-practice/lesson-64
git switch -q feature-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --graph --all
```

`feature-tea` has two commits: the latte price (which conflicts with `main`) and green tea (which does not).

## Demonstration

<!-- test: fail; contains=CONFLICT (content): Merge conflict in prices.txt; output -->
```bash
git rebase main 2>&1 | grep -v "^hint:"
test "${PIPESTATUS[0]}" -eq 0
```

```text
Rebasing (1/2)
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
error: could not apply 00931cc... Raise the latte price to 3.50
Could not apply 00931cc... # Raise the latte price to 3.50
```

Where are we?

<!-- test: contains=rebase in progress; output -->
```bash
git status
```

```text
interactive rebase in progress; onto 594657b
Last command done (1 command done):
   pick 00931cc # Raise the latte price to 3.50
Next command to do (1 remaining command):
   pick 235b134 # Add green tea
  (use "git rebase --edit-todo" to view and edit)
You are currently rebasing branch 'feature-tea' on '594657b'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

The status shows the commit being replayed ("Raise the latte price to 3.50") and the one still to do. The file:

<!-- test: contains=<<<<<<<; output -->
```bash
cat prices.txt
```

```text
espresso 2.50
<<<<<<< HEAD
latte 3.30
=======
latte 3.50
>>>>>>> 00931cc (Raise the latte price to 3.50)
cappuccino 3.40
```

`HEAD` is `main`'s version (3.30, Grace); the other side is your commit being replayed (3.50). The team agreed on 3.40:

<!-- test: contains=Successfully rebased; output -->
```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git rebase --continue
git log --oneline --graph -4
```

```text
[detached HEAD cff42b7] Raise the latte price to 3.50
 1 file changed, 1 insertion(+), 1 deletion(-)
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
* 2457385 (HEAD -> feature-tea) Add green tea
* cff42b7 Raise the latte price to 3.50
* 594657b (main) Raise the latte price to 3.30
* 4267004 Add prices
```

(`git rebase --continue` opens the editor for the commit message; here it is kept as is.) Then the second commit was
replayed without a conflict.

## Command breakdown

| Command | Use during a rebase |
|---|---|
| `git status` | which commit is being replayed, which files conflict |
| `git diff` | the unresolved conflicts |
| `git add FILE` | mark FILE resolved |
| `git rebase --continue` | commit the resolution, replay the next commit |
| `git rebase --skip` | drop the current commit entirely |
| `git rebase --abort` | return to the state before the rebase (lesson 65) |
| `git checkout --ours/--theirs FILE` | take main's / your commit's version (note the reversed meaning) |

## Hands-on exercise

**Instructions.** Check that the rebased commit still carries its original message and author.

**Expected result.** "Raise the latte price to 3.50" by Ada Lovelace (although the price is now 3.40: consider
rewording it, lesson 63).

**Verification.**

<!-- test: contains=Ada Lovelace -->
```bash
cd ~/git-practice/lesson-64
git log -2 --format='%s by %an'
```

## Break it

Recreate the conflict (`ORIG_HEAD` is the branch before the rebase), edit the file, and continue **without** `git add`:

<!-- test: fail; contains=mark them as resolved using git add; output -->
```bash
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git rebase --continue 2>&1
```

```text
prices.txt: needs merge
You must edit all merge conflicts and then
mark them as resolved using git add
```

## Troubleshoot

Git does not look at the file content to decide whether you are done; it looks at the index. Until `git add` marks
the file resolved, it is still "unmerged":

<!-- test: contains=both modified; output -->
```bash
git status --short
git status | grep "both modified"
```

```text
UU prices.txt
	both modified:   prices.txt
```

## Fix

<!-- test: contains=Successfully rebased; output -->
```bash
git add prices.txt
git rebase --continue
```

```text
[detached HEAD cff42b7] Raise the latte price to 3.50
 1 file changed, 1 insertion(+), 1 deletion(-)
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
```

## Real-world example

Rebasing a long-lived branch with 20 commits onto a busy `main` can mean resolving the same conflict at several
commits. Two tools help: `git config --global rerere.enabled true` ("reuse recorded resolution": Git remembers how you
resolved a conflict and re-applies it), and squashing the branch first (lesson 63) so there is only one commit to
replay.

## Practice challenge

Enable `rerere`, resolve the conflict once, then abort the rebase, start it again, and watch Git resolve it for you.

<details>
<summary>Solution</summary>

<!-- test: contains=Resolved 'prices.txt' using previous resolution; output -->
```bash
cd ~/git-practice/lesson-64
git config rerere.enabled true
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
git rebase main 2>&1 | grep -i "resolved" || true
git rebase --abort
```

```text
Recorded resolution for 'prices.txt'.
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
hint: Resolve all conflicts manually, mark them as resolved with
Resolved 'prices.txt' using previous resolution.
```

</details>

## Recap

- A rebase stops at each conflicting commit; `git status` says which one.
- Fix → `git add` → `git rebase --continue`; `--skip` drops the commit, `--abort` cancels.
- During a rebase, "ours" is the new base and "theirs" is your commit.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-64
```

Next: [Lesson 65 · Aborting a rebase](../65-abort-rebase/README.md).
