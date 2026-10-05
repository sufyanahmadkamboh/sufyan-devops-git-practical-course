# Lesson 67 · Cherry-pick

> Level 14 · Advanced Git · ⏱ 20 minutes

## What are we learning?

`git cherry-pick COMMIT` copies the change of one commit onto the current branch, as a new commit. The classic use:
an important bug fix was made on a feature branch, and production needs that fix **now**, without the rest of the
unfinished feature.

## Visual

```text
 feature    A ── B ── F1 ── FIX ── F2        F1, F2: unfinished feature work · FIX: an urgent bug fix
                 │
 production      B                           git switch production
                 │                           git cherry-pick FIX
                 B ── FIX'                   FIX' = same change, new commit on production; F1, F2 stay behind
```

## Lab setup

<!-- test: contains=lesson-67 -->
```bash
bash scripts/new-lab.sh lesson-67 basic
cd ~/git-practice/lesson-67
git branch production
git switch -q -c feature-specials
echo "Monday: mocha" > specials.txt && git add specials.txt && git commit -q -m "Start the specials board"
sed -i 's/cappuccino 3.40/cappuccino 3.50/' prices.txt && git commit -q -am "Fix the cappuccino price (charged too little)"
echo "Tuesday: chai" >> specials.txt && git commit -q -am "Add Tuesday special"
git log --oneline --graph --all
```

## Demonstration

Production needs the price fix only:

<!-- test: contains=Fix the cappuccino price; output -->
```bash
fix=$(git log --format=%h --grep="Fix the cappuccino price" feature-specials)
git switch -q production
git cherry-pick "$fix"
git log --oneline -2
ls
```

```text
[production 03492fb] Fix the cappuccino price (charged too little)
 Date: Mon Oct 5 03:49:31 2026 +0200
 1 file changed, 1 insertion(+), 1 deletion(-)
03492fb (HEAD -> production) Fix the cappuccino price (charged too little)
4267004 (main) Add prices
README.md
menu.txt
prices.txt
```

`specials.txt` is not on production: only the fix came along. The cherry-picked commit has a new ID but the same change:

<!-- test: output -->
```bash
git show "$fix" | git patch-id | cut -c1-12
git show HEAD | git patch-id | cut -c1-12
```

```text
fatal: ambiguous argument '': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
6ed7d7cd1b92
```

## Command breakdown

| Command | What it does |
|---|---|
| `git cherry-pick C` | apply C's change as a new commit on the current branch |
| `git cherry-pick -x C` | add "(cherry picked from commit …)" to the message |
| `git cherry-pick A^..B` | a range, oldest first (A included) |
| `git cherry-pick --no-commit C` | apply without committing |
| `git cherry-pick --continue / --abort / --skip` | after a conflict |

## Hands-on exercise

**Instructions.** Find the commits on `feature-specials` that production does **not** have an equivalent of
(`git cherry`).

**Expected result.** Two `+` lines (the specials commits) and one `-` line (the fix, already applied).

**Verification.**

<!-- test: contains=- ; contains=+ -->
```bash
cd ~/git-practice/lesson-67
git cherry -v production feature-specials
```

## Break it

Production also wants the Tuesday special:

<!-- test: fail; contains=CONFLICT (modify/delete); output -->
```bash
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)" 2>&1
```

```text
CONFLICT (modify/delete): specials.txt deleted in HEAD and modified in ea104e4 (Add Tuesday special).  Version ea104e4 (Add Tuesday special) of specials.txt left in tree.
error: could not apply ea104e4... Add Tuesday special
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git cherry-pick --continue".
hint: You can instead skip this commit with "git cherry-pick --skip".
hint: To abort and get back to the state before "git cherry-pick",
hint: run "git cherry-pick --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
```

## Troubleshoot

`CONFLICT (modify/delete): specials.txt deleted in HEAD and modified in …`: the Tuesday commit **modifies**
`specials.txt`, a file created by an earlier commit ("Start the specials board") that production does not have. A
cherry-picked commit carries only its own change, not the commits it depends on.

## Fix

Abort, and pick the dependency first, in order (a range):

<!-- test: contains=Tuesday: chai; output -->
```bash
git cherry-pick --abort
start=$(git log --format=%h --grep='Start the specials' feature-specials)
git cherry-pick "$start"
git cherry-pick "$(git log --format=%h --grep='Tuesday' feature-specials)"
cat specials.txt
```

```text
[production 9ab5895] Start the specials board
 Date: Mon Oct 5 03:49:31 2026 +0200
 1 file changed, 1 insertion(+)
 create mode 100644 specials.txt
[production 876cc7e] Add Tuesday special
 Date: Mon Oct 5 03:49:31 2026 +0200
 1 file changed, 1 insertion(+)
Monday: mocha
Tuesday: chai
```

## Real-world example

Release branches: `release/2.4` is in production; a security fix is merged to `main`. The fix is cherry-picked with
`-x` onto `release/2.4` (`git cherry-pick -x <sha>`), tagged `v2.4.1` and deployed, while `main` continues towards 2.5.
The `-x` line lets anyone trace the backport to the original commit.

## Practice challenge

Cherry-pick the fix again onto a new branch `release-1.0` from `4267004`, recording where it came from.

<details>
<summary>Solution</summary>

<!-- test: contains=cherry picked from commit; output -->
```bash
cd ~/git-practice/lesson-67
git switch -q -c release-1.0 4267004
git cherry-pick -x "$(git log --format=%h --grep='Fix the cappuccino' feature-specials)" > /dev/null
git log -1 --format=%B
```

```text
Fix the cappuccino price (charged too little)

(cherry picked from commit 702fad1e348bc4b10b305335569269d691d57816)
```

</details>

## Recap

- `git cherry-pick C` copies one commit's change onto the current branch as a new commit.
- It does not bring the commits C depends on: pick those first, in order.
- Use `-x` for backports; prefer merging when you want everything.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-67
```

Next: [Lesson 68 · Git tags](../68-git-tags/README.md).
