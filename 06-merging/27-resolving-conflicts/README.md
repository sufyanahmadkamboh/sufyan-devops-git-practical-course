# Lesson 27 · Resolving merge conflicts

> Level 5 · Merging · ⏱ 20 minutes

## What are we learning?

The resolution loop: decide the right content, edit the file, `git add` it, commit the merge. And the shortcuts for
"take mine" or "take theirs" for a whole file.

## Visual

```text
 git merge X ──► CONFLICT ──► edit the file (remove ALL markers, keep the right content)
                                 │
                                 ▼
                             git add FILE          ← "this file is resolved"
                                 │
                                 ▼
                             git commit            ← records the merge (two parents)
```

## Lab setup

<!-- test: contains=lesson-27 -->
```bash
bash scripts/new-lab.sh lesson-27 conflict
cd ~/git-practice/lesson-27
git merge feature-tea > /dev/null 2>&1 || git status --short
```

## Demonstration

The conflict: main says 3.30, feature-tea says 3.50. After asking the team, the decision is 3.40, which is neither
side. Write the file as it should be, without any marker:

<!-- test: contains=latte 3.40; output -->
```bash
cat prices.txt
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
cat prices.txt
```

```text
espresso 2.50
<<<<<<< HEAD
latte 3.30
=======
latte 3.50
>>>>>>> feature-tea
cappuccino 3.40
espresso 2.50
latte 3.40
cappuccino 3.40
```

Mark it resolved and commit:

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
git add prices.txt
git status --short
git commit -q --no-edit
git log --oneline --graph -4
```

```text
M  prices.txt
*   49a8b38 (HEAD -> main) Merge branch 'feature-tea'
|\  
| * 00931cc (feature-tea) Raise the latte price to 3.50
* | 594657b Raise the latte price to 3.30
|/  
* 4267004 Add prices
```

`--no-edit` keeps Git's prepared message ("Merge branch 'feature-tea'"); without it, your editor opens with that
message, where you can add a line explaining the decision.

## Command breakdown

| Command | Use |
|---|---|
| `git status` | which files are still "both modified" |
| edit, then `git add FILE` | mark a file resolved |
| `git commit` | conclude the merge |
| `git checkout --ours FILE` / `--theirs FILE` | take one side's whole file, then `git add` it |
| `git diff` during a merge | combined diff of what is still unresolved |
| `git mergetool` | open a configured visual merge tool |

## Hands-on exercise

**Instructions.** Recreate the conflict (a fresh lab) and resolve it by keeping **their** version (`feature-tea`'s
3.50) for the whole file, without typing the content.

**Expected result.** `latte 3.50`, a merge commit.

<!-- test-run: true -->

**Verification.**

<!-- test: contains=latte 3.50 -->
```bash
cd ~/git-practice/lesson-27
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git checkout --theirs prices.txt && git add prices.txt && git commit -q --no-edit
grep latte prices.txt
```

## Break it

Resolve carelessly: "resolve" by staging the file with the markers still in it.

<!-- test: contains=<<<<<<< HEAD -->
```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git add prices.txt
git commit -q --no-edit
cat prices.txt
```

## Troubleshoot

Git accepted it: `git add` means "resolved" whatever the content. The markers are now **committed**, and anything that
reads `prices.txt` breaks. Find committed markers before they spread:

<!-- test: contains=leftover conflict marker -->
```bash
git diff --check HEAD~1 HEAD 2>&1 | head -3 || true
grep -n '^<<<<<<<\|^=======\|^>>>>>>>' prices.txt
```

`git diff --check` reports "leftover conflict marker".

## Fix

The merge is not pushed: redo it properly. Undo the bad merge commit, merge again, resolve for real:

<!-- test: contains=latte 3.40; absent=<<<; output -->
```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q --no-edit
cat prices.txt
```

```text
espresso 2.50
latte 3.40
cappuccino 3.40
```

## Real-world example

Before finishing a merge in a real project, run what CI would run (tests, `helm lint`, `terraform validate`, a build):
a conflict resolution is new code that nobody has reviewed yet. Many teams add a CI check that fails on leftover
conflict markers, exactly like `git diff --check`.

## Practice challenge

Configure Git to refuse commits that contain conflict markers, using a hook that runs `git diff --cached --check`
(hooks are lesson 82; this is a preview).

<details>
<summary>Solution</summary>

<!-- test: fail; contains=leftover conflict marker; output -->
```bash
cd ~/git-practice/lesson-27
printf '#!/bin/sh\nexec git diff --cached --check\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
printf '<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> other\n' > test.txt && git add test.txt
git commit -m "Test" 2>&1
```

```text
test.txt:1: leftover conflict marker
test.txt:3: leftover conflict marker
test.txt:5: leftover conflict marker
```

</details>

## Recap

- Resolve = write the correct content, remove every marker, `git add`, `git commit`.
- `--ours`/`--theirs` take one side's whole file.
- `git add` trusts you: check for leftover markers (`git diff --check`) and test before committing.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-27
```

Next: [Lesson 28 · Aborting a merge](../28-abort-merge/README.md).
