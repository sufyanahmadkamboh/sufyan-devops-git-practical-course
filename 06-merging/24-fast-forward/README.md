# Lesson 24 · Fast-forward merge

> Level 5 · Merging · ⏱ 15 minutes

## What are we learning?

When the current branch has not moved since the other branch started, a merge does not need a merge commit: Git simply
moves the label forward. That is a fast-forward. We also see how to refuse it (`--no-ff`) and how to require it
(`--ff-only`).

## Visual

```text
 before                                  after git merge feature (fast-forward)

 A ── B  ← main                          A ── B ── C  ← main, feature
       ╲                                 (main's label just moved to C: no new commit)
        C  ← feature
```

## Lab setup

<!-- test: contains=lesson-24 -->
```bash
bash scripts/new-lab.sh lesson-24 feature
cd ~/git-practice/lesson-24
git log --oneline --graph --all
```

## Demonstration

<!-- test: contains=Fast-forward; output -->
```bash
git merge feature-tea
git log --oneline --graph --all
```

```text
Updating 4267004..bb67674
Fast-forward
 menu.txt | 1 +
 1 file changed, 1 insertion(+)
* bb67674 (HEAD -> main, feature-tea) Add green tea to the menu
* 4267004 Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

`Fast-forward`: no merge commit; `main` and `feature-tea` point to the same commit. The history stays a straight line.

Some teams want every feature to be visible as a merge, even when a fast-forward is possible:

<!-- test: contains=Merge branch 'feature-hours'; output -->
```bash
git switch -q -c feature-hours && echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add hours"
git switch -q main
git merge --no-ff --no-edit feature-hours
git log --oneline --graph -4
```

```text
Merge made by the 'ort' strategy.
 hours.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 hours.txt
*   d986fad (HEAD -> main) Merge branch 'feature-hours'
|\  
| * be5c323 (feature-hours) Add hours
|/  
* bb67674 (feature-tea) Add green tea to the menu
* 4267004 Add prices
```

`--no-ff` created a merge commit anyway: the history records that "Add hours" came from a branch.

## Command breakdown

| Command | Behaviour |
|---|---|
| `git merge X` | fast-forward if possible, merge commit otherwise |
| `git merge --no-ff X` | always a merge commit |
| `git merge --ff-only X` | only fast-forward; refuse if a merge commit would be needed |
| `git config merge.ff only` | make `--ff-only` the default |

## Hands-on exercise

**Instructions.** Create a branch with one commit and merge it with `--ff-only`.

**Expected result.** `Fast-forward`, and no merge commit.

<!-- test-run: cd ~/git-practice/lesson-24 && git switch -q -c feature-chai && echo chai >> menu.txt && git commit -q -am "Add chai" && git switch -q main && git merge -q --ff-only feature-chai -->

**Verification.**

<!-- test: contains=Add chai -->
```bash
cd ~/git-practice/lesson-24
git log --oneline -1
git log --oneline --merges | wc -l
```

## Break it

`--ff-only` when the branches have diverged:

<!-- test: fail; contains=Not possible to fast-forward; output -->
```bash
git switch -q -c feature-mocha HEAD~1 && echo "mocha 3.90" >> prices.txt && git commit -q -am "Price mocha"
git switch -q main
git merge --ff-only feature-mocha 2>&1
```

```text
hint: Diverging branches can't be fast-forwarded, you need to either:
hint:
hint: 	git merge --no-ff
hint:
hint: or:
hint:
hint: 	git rebase
hint:
hint: Disable this message with "git config set advice.diverging false"
fatal: Not possible to fast-forward, aborting.
```

## Troubleshoot

`fatal: Not possible to fast-forward, aborting.`: `main` has a commit (`Add chai`) that `feature-mocha` does not, so
`main` cannot simply move forward to it. The branches have diverged:

<!-- test: output -->
```bash
git log --oneline --graph main feature-mocha | head -5
```

```text
* 45d6d00 (HEAD -> main, feature-chai) Add chai
| * 97d7b53 (feature-mocha) Price mocha
|/  
*   d986fad Merge branch 'feature-hours'
|\  
```

## Fix

Two valid choices: allow a merge commit (`git merge feature-mocha`), or first replay the branch on top of `main` so a
fast-forward becomes possible (rebase, lesson 61). With the rebase:

<!-- test: contains=Fast-forward; output -->
```bash
git switch -q feature-mocha
git rebase -q main
git switch -q main
git merge --ff-only feature-mocha
```

```text
Updating 45d6d00..8109406
Fast-forward
 prices.txt | 1 +
 1 file changed, 1 insertion(+)
```

## Real-world example

Pull requests on GitHub can be configured to allow "merge commits", "squash merging" or "rebase merging" (lesson 54).
`git pull` can be configured the same way locally: `git config pull.ff only` makes `git pull` refuse to create
surprise merge commits on your `main`, which is a common team setting.

## Practice challenge

Undo the last fast-forward merge on `main` (the label should move back to where it was before) without losing the
branch's commit.

<details>
<summary>Solution</summary>

<!-- test: contains=feature-mocha; output -->
```bash
cd ~/git-practice/lesson-24
git reset -q --hard ORIG_HEAD
git log --oneline --graph -3 main feature-mocha
```

```text
* 8109406 (feature-mocha) Price mocha
* 45d6d00 (HEAD -> main, feature-chai) Add chai
*   d986fad Merge branch 'feature-hours'
|\  
```

A merge records the previous position of the branch in `ORIG_HEAD`. Moving `main` back is safe here because nothing was
pushed; the commits still exist on `feature-mocha` (lesson 31 explains `reset`).

</details>

## Recap

- Fast-forward: the current branch had not moved, so its label just moves forward. No merge commit.
- `--no-ff` forces a merge commit; `--ff-only` refuses anything but a fast-forward.
- Diverged branches cannot fast-forward: merge with a commit, or rebase first.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-24
```

Next: [Lesson 25 · Three-way merge](../25-three-way-merge/README.md).
