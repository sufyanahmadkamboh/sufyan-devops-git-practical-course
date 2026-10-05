# Lesson 32 · git revert

> Level 6 · Undoing changes · ⏱ 20 minutes

## What are we learning?

`git revert COMMIT` creates a **new** commit that undoes an earlier one. History is not rewritten, so it is the safe way
to undo something that is already shared (pushed to `main`, deployed).

## Visual

```text
 reset (rewrites):    A ── B ── C        →   A ── B            C disappears from the branch

 revert (adds):       A ── B ── C        →   A ── B ── C ── C'  C' = the exact opposite of C
                                                                 everyone can pull it normally
```

## Lab setup

<!-- test: contains=lesson-32 -->
```bash
bash scripts/new-lab.sh lesson-32 history
cd ~/git-practice/lesson-32
git log --oneline
```

## Demonstration

The mocha machine broke, and "Add mocha" is already on the shared `main`. Take mocha off the menu by reverting it:

<!-- test: contains=Revert "Add mocha"; output -->
```bash
target=$(git log --format=%h --grep="^Add mocha")
git revert --no-edit "$target"
git log --oneline -3
```

```text
[main 3df45fb] Revert "Add mocha"
 Date: Mon Oct 5 03:32:50 2026 +0200
 1 file changed, 1 deletion(-)
3df45fb (HEAD -> main) Revert "Add mocha"
ecff18a Price mocha
2c389c0 Add mocha
```

The revert is a normal commit; look at what it does:

<!-- test: contains=-mocha; output -->
```bash
git show --format='%s%n%b' HEAD
```

```text
Revert "Add mocha"
This reverts commit 2c389c05c38cabc31d37906c2bb6b6d938959226.


diff --git a/menu.txt b/menu.txt
index 623a4cc..cbd8549 100644
--- a/menu.txt
+++ b/menu.txt
@@ -2,4 +2,3 @@ espresso
 latte
 cappuccino
 green tea
-mocha
```

The commit after it ("Price mocha") is untouched: revert undoes **one** commit's change, wherever it is
in the history.

## Command breakdown

| Command | What it does |
|---|---|
| `git revert C` | new commit undoing C (opens the editor for the message) |
| `git revert --no-edit C` | keep the default message `Revert "..."` |
| `git revert --no-commit C1 C2` | undo several, commit once yourself |
| `git revert -m 1 MERGE` | undo a merge commit, keeping parent 1 (`main`) |
| `git revert --abort` / `--continue` | when the revert conflicts |

## Hands-on exercise

**Instructions.** Revert the revert: the machine is repaired.

**Expected result.** `mocha` is back in `menu.txt`, and the history shows both reverts.

<!-- test-run: cd ~/git-practice/lesson-32 && git revert --no-edit HEAD > /dev/null -->

**Verification.**

<!-- test: contains=mocha -->
```bash
cd ~/git-practice/lesson-32
grep mocha menu.txt
git log --oneline -2
```

## Break it

Revert a commit whose lines were changed again later: "Add green tea" added `green tea` to `menu.txt`, and later commits
changed that line.

<!-- test: fail; contains=CONFLICT; output -->
```bash
sed -i 's/^green tea$/green tea (organic)/' menu.txt && git commit -q -am "Organic green tea"
git revert --no-edit "$(git log --format=%h --grep='^Add green tea')" 2>&1
```

```text
Auto-merging menu.txt
CONFLICT (content): Merge conflict in menu.txt
error: could not revert 6833580... Add green tea
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git revert --continue".
hint: You can instead skip this commit with "git revert --skip".
hint: To abort and get back to the state before "git revert",
hint: run "git revert --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
```

## Troubleshoot

A revert is a merge of the "opposite" change: if the same lines changed afterwards, it conflicts exactly like a merge
(lesson 26). `git status` says "You are currently reverting commit ...":

<!-- test: contains=currently reverting; output -->
```bash
git status | head -4
```

```text
On branch main
You are currently reverting commit 6833580.
  (fix conflicts and run "git revert --continue")
  (use "git revert --skip" to skip this patch)
```

## Fix

Decide what the file should be (here: no green tea at all), resolve, continue:

<!-- test: absent=green tea; output -->
```bash
grep -v -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>' -e 'green tea' -e '^|||||||' menu.txt > menu.tmp && mv menu.tmp menu.txt
git add menu.txt
git revert --continue > /dev/null
cat menu.txt
```

```text
espresso
latte
cappuccino
mocha
```

Or `git revert --abort` to cancel and return to the state before the revert.

## Real-world example

A release deployed from `main` breaks production; the cause is one merged pull request. `git revert -m 1 <merge>`
creates a commit undoing the whole PR, CI deploys it, production is fixed in minutes, and the history clearly records
what happened. GitHub has a "Revert" button on merged pull requests that does exactly this through a new PR.

## Practice challenge

Undo the last two commits with a **single** revert commit.

<details>
<summary>Solution</summary>

<!-- test: contains=Revert the last two commits; output -->
```bash
cd ~/git-practice/lesson-32
git revert --no-commit HEAD~1..HEAD
git commit -q -m "Revert the last two commits"
git log --oneline -1
```

```text
05608e7 (HEAD -> main) Revert the last two commits
```

</details>

## Recap

- `revert` undoes a commit by adding its opposite; history is kept.
- Use revert for anything already pushed; reset only for local, unshared commits.
- Reverts can conflict: resolve, `git add`, `git revert --continue`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-32
```

Next: [Lesson 33 · git reflog](../33-git-reflog/README.md).
