# Module 06 · Merging · Assessment

> Lessons 23–28 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-06-practical diverged
bash scripts/new-lab.sh assess-06-broken conflict
```

## Quiz

1. You are on `main` and run `git merge feature`. Which branch moves?
2. When does `git merge` create no merge commit at all?
3. What does `git merge --ff-only` do when the branches have diverged?
4. What is the merge base, and how do you show it?
5. Both branches changed **different** lines of the same file. Is there a conflict?
6. In a conflicted file, what is between `<<<<<<< HEAD` and `=======`?
7. You resolved the file content. What tells Git the conflict is resolved?
8. Which command returns you to the state before a merge that went badly?

<details>
<summary>Answers</summary>

1. `main`, the current branch; `feature` stays where it is (lesson 23).
2. When the current branch has not moved since the other branch started: a fast-forward (lesson 24).
3. It refuses with `Not possible to fast-forward, aborting.` and changes nothing (lesson 24).
4. The last commit both branches share; `git merge-base A B` (lesson 25).
5. No: changes to different lines are combined automatically (lesson 25).
6. The version of the branch you are on (`HEAD`, "ours") (lesson 26).
7. `git add FILE` (then `git commit` concludes the merge) (lesson 27).
8. `git merge --abort` (lesson 28).

</details>

## Practical challenge

In `~/git-practice/assess-06-practical`:

1. Merge `feature-tea` into `main` with a merge commit.
2. Create a branch `feature-chai` from `main` that adds a new file `chai.txt`, and merge it into `main` with
   `--ff-only` (no merge commit for this one).
3. Delete both merged branches with `git branch -d`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
cd ~/git-practice/assess-06-practical
git merge -q --no-edit feature-tea
git switch -q -c feature-chai
echo "chai 3.10" > chai.txt && git add chai.txt && git commit -q -m "Add chai"
git switch -q main && git merge -q --ff-only feature-chai
git branch -d feature-tea feature-chai
git log --oneline --graph -5
```

```text
Deleted branch feature-tea (was bb67674).
Deleted branch feature-chai (was abb8114).
* abb8114 (HEAD -> main) Add chai
*   bc5e27a Merge branch 'feature-tea'
|\  
| * bb67674 Add green tea to the menu
* | f40d080 Add opening hours
|/  
* 4267004 Add prices
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-06-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "exactly one merge commit on main"   '[ "$(git rev-list --merges --count main)" -eq 1 ]'
check "chai.txt on main, no merge for it"  '[ "$(git log -1 --format=%s main)" = "Add chai" ]'
check "green tea merged"                   'grep -q "green tea" menu.txt'
check "merged branches deleted"            '[ "$(git branch | wc -l)" -eq 1 ]'
```

```text
ok       exactly one merge commit on main
ok       chai.txt on main, no merge for it
ok       green tea merged
ok       merged branches deleted
```

## Troubleshooting challenge

A colleague started a merge in `~/git-practice/assess-06-broken` and left for lunch:

<!-- test: fail; contains=CONFLICT; output -->
```bash
cd ~/git-practice/assess-06-broken
git merge feature-tea 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

Symptom: nothing can be committed.

<!-- test: fail; contains=unmerged files; output -->
```bash
git commit -m "Save my work" 2>&1
```

```text
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U	prices.txt
```

Finish the merge correctly: the team agreed on a latte price of **3.40**.

<details>
<summary>Solution</summary>

`git status` shows `both modified: prices.txt`: the latte line was changed on both branches. Write the agreed
content, mark it resolved, commit:

<!-- test: contains=latte 3.40; output -->
```bash
git status --short
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git commit -q --no-edit
cat prices.txt
```

```text
UU prices.txt
espresso 2.50
latte 3.40
cappuccino 3.40
```

</details>

Verification:

<!-- test: contains=no markers; contains=Merge branch 'feature-tea'; output -->
```bash
git grep -qE '^(<<<<<<<|=======|>>>>>>>)' && echo "markers left" || echo "no markers"
git log --oneline -1
```

```text
no markers
de6d6da (HEAD -> main) Merge branch 'feature-tea'
```

## Real-world scenario

Your feature branch has been open for two weeks. Before opening the PR you merge `main` into it and get conflicts in
eleven files, several of them in code you do not know. What do you do?

<details>
<summary>Model answer</summary>

`git merge --abort` to get back to a clean state (lesson 28). Then reduce the problem: merge `main` in smaller steps
(`git merge <older main commit>` first), or rebase/squash your own commits so there are fewer to reconcile. For files
you do not know, look at who changed them (`git log --merge -- FILE`) and ask those people. Resolve with
`merge.conflictStyle zdiff3` to see the base, run the tests before committing, and next time merge `main` in daily so
conflicts stay small (lesson 56).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-06-practical ~/git-practice/assess-06-broken
```
