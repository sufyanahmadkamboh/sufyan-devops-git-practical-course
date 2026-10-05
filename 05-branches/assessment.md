# Module 05 · Branches · Assessment

> Lessons 17–22 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-05-branches basic
bash scripts/new-lab.sh assess-05-broken diverged
```

## Quiz

1. What is a branch, technically?
2. Which single command creates a branch and switches to it?
3. What does `git branch` (without arguments) show, and what does `*` mean?
4. What happens to uncommitted changes when you switch branches and the files do not differ between the branches?
5. Why does `git branch -d NAME` sometimes refuse, and what does `-D` do differently?
6. Can you delete the branch you are currently on?
7. Which command shows every branch's last commit?

<details>
<summary>Answers</summary>

1. A movable name pointing at a commit (lessons 17, 77).
2. `git switch -c NAME` (lesson 20).
3. The local branches; `*` marks the current one (lesson 18).
4. They come along to the other branch (lesson 19).
5. `-d` refuses branches whose commits are not merged anywhere; `-D` deletes anyway (lesson 22).
6. No: switch to another branch first (lesson 22).
7. `git branch -v` (lesson 21).

</details>

## Practical challenge

In `assess-05-branches`, create `feature-chai` with one commit adding chai to the menu, and `experiment` with one commit
that you then decide to throw away. End on `main`, with `feature-chai` kept and `experiment` deleted.

<details>
<summary>Reference solution</summary>

<!-- test: contains=feature-chai; output -->
```bash
cd ~/git-practice/assess-05-branches
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git switch -q main && git switch -q -c experiment && echo "idea" > idea.txt && git add idea.txt && git commit -q -m "Try an idea"
git switch -q main
git branch -D experiment
git branch -v
```

```text
Deleted branch experiment (was 41814f9).
  feature-chai 7667408 Add chai
* main         4267004 Add prices
```

</details>

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-05-branches
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "on main"                        '[ "$(git branch --show-current)" = main ]'
check "feature-chai has the chai commit" 'git log --format=%s main..feature-chai | grep -qx "Add chai"'
check "experiment is deleted"          '! git rev-parse -q --verify refs/heads/experiment'
check "main has no chai yet"           '! grep -q chai menu.txt'
```

```text
ok       on main
ok       feature-chai has the chai commit
ok       experiment is deleted
ok       main has no chai yet
```

## Troubleshooting challenge

In `assess-05-broken`, you edit `README.md` on `feature-tea`, then try to switch to `main` to check something:

<!-- test: contains=lab -->
```bash
cd ~/git-practice/assess-05-broken
git switch -q feature-tea
echo "Tea is served all day." >> README.md
echo "lab: README edited on feature-tea"
```

Symptom:

<!-- test: fail; contains=would be overwritten by checkout; output -->
```bash
git switch main 2>&1
```

```text
error: Your local changes to the following files would be overwritten by checkout:
	README.md
Please commit your changes or stash them before you switch branches.
Aborting
```

<details>
<summary>Solution</summary>

`README.md` differs between the two branches (main added opening hours), so switching would overwrite your edit;
Git refuses. Commit the edit on the branch where it belongs (or stash it, lesson 34), then switch:

<!-- test: contains=main; output -->
```bash
git commit -q -am "Mention tea all day"
git switch main
git branch --show-current
```

```text
Switched to branch 'main'
main
```

</details>

## Real-world scenario

You are halfway through a feature when a teammate asks you to check a bug on `main` right now. Your changes are not
ready to commit. What are your options, and which would you choose?

<details>
<summary>Model answer</summary>

If the changed files are the same on both branches, `git switch main` simply carries the changes along (careful not
to commit them there). If Git refuses, options are: commit a "WIP" commit on the feature branch and amend it later;
`git stash` and `git stash pop` afterwards (lesson 34); or a second working directory with `git worktree add`
(lesson 87). A WIP commit or a worktree is the safest: nothing is hidden in a stash you might forget.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-05-branches ~/git-practice/assess-05-broken
```
