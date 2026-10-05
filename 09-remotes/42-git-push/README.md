# Lesson 42 · git push

> Level 8 · Remote repositories · ⏱ 20 minutes

## What are we learning?

`git push` uploads your commits and moves the branch on the server. It only works as a fast-forward; when someone
pushed before you, it is rejected. We see why, the right fix, and the safe way to force-push your own branch.

## Visual

```text
 server main: A ── B ── C   (Grace's C)
 your main:   A ── B ── X   (your X)

 git push → rejected: moving the server's main to X would throw away C
 fix:       git pull (merge/rebase) → A ── B ── C ── X'  → git push ✓

 --force             overwrite whatever is there (C is lost on the server!)
 --force-with-lease  overwrite only if the server still has what I last fetched
```

## Lab setup

<!-- test: contains=lesson-42 -->
```bash
bash scripts/new-lab.sh lesson-42 remote
cd ~/git-practice/lesson-42/ada
```

## Demonstration

<!-- test: contains=main -> main; output -->
```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git push
```

```text
To ~/git-practice/lesson-42/server/cafe.git
   4267004..d4540f4  main -> main
```

`4267004..xxxxxxx  main -> main`: the server's `main` moved from the old commit to the new one. Push a new branch:

<!-- test: contains=[new branch]; output -->
```bash
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push origin feature-chai
```

```text
To ~/git-practice/lesson-42/server/cafe.git
 * [new branch]      feature-chai -> feature-chai
```

## Command breakdown

| Command | What it does |
|---|---|
| `git push` | push the current branch to its upstream (lesson 43) |
| `git push origin BRANCH` | push BRANCH to origin |
| `git push -u origin BRANCH` | push and set the upstream |
| `git push origin --delete BRANCH` | delete a branch on the server |
| `git push --tags` / `origin TAG` | push tags (lesson 69) |
| `git push --force-with-lease` | replace the remote branch, only if nobody else changed it |

## Hands-on exercise

**Instructions.** Delete `feature-chai` on the server (it was merged elsewhere), keep it locally.

**Expected result.** `git ls-remote --heads origin` lists only `main`.

<!-- test-run: cd ~/git-practice/lesson-42/ada && git push -q origin --delete feature-chai -->

**Verification.**

<!-- test: absent=feature-chai -->
```bash
cd ~/git-practice/lesson-42/ada
git ls-remote --heads origin
```

## Break it

Grace pushes first; then Ada:

<!-- test: fail; contains=[rejected]; contains=fetch first; output -->
```bash
cd ../grace && git pull -q && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git push 2>&1
```

```text
To ~/git-practice/lesson-42/server/cafe.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '~/git-practice/lesson-42/server/cafe.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Troubleshoot

`! [rejected] main -> main (fetch first)`: the server's `main` has a commit (Grace's) that Ada does not have. A push
must be a fast-forward of the server's branch; accepting Ada's push would delete Grace's commit from `main`.
(`non-fast-forward` is the same rejection when Git already knows the remote commit from an earlier fetch.)

## Fix

Integrate first, then push. **Not** `--force`.

<!-- test: contains=main -> main; output -->
```bash
git pull -q --rebase
git push
git log --oneline -3
```

```text
To ~/git-practice/lesson-42/server/cafe.git
   c234723..3f3ebb8  main -> main
3f3ebb8 (HEAD -> main, origin/main, origin/HEAD) Espresso 2.60
c234723 Add mocha
d4540f4 Add green tea
```

Both commits are on the server: Grace's, then Ada's on top.

## Real-world example

After rebasing **your own** feature branch (lesson 61), its pushed version no longer matches, and a normal push is
rejected. Use `git push --force-with-lease`: it refuses if someone else pushed to your branch in the meantime, whereas
`--force` would silently delete their work. Never force-push `main`; protect it on GitHub (lesson 59) so nobody can.

## Practice challenge

Show that `--force-with-lease` protects Grace's work: Ada rewrites her last commit and force-pushes with lease after
Grace pushed something new that Ada has not fetched.

<details>
<summary>Solution</summary>

<!-- test: contains=stale info; output -->
```bash
cd ~/git-practice/lesson-42/grace && git pull -q && echo "chai" >> menu.txt && git commit -q -am "Add chai" && git push -q
cd ../ada && git commit -q --amend -m "Raise the espresso price to 2.60"
git push --force-with-lease 2>&1 || true
```

```text
To ~/git-practice/lesson-42/server/cafe.git
 ! [rejected]        main -> main (stale info)
error: failed to push some refs to '~/git-practice/lesson-42/server/cafe.git'
```

`(stale info)`: the server's `main` is not where Ada's `origin/main` says it was, so the push is refused. `--force`
would have succeeded and removed "Add chai".

</details>

## Recap

- A push must fast-forward the server's branch; otherwise it is rejected.
- Fix a rejection with `git pull` (merge or rebase), then push again.
- Only rewrite pushed history on your own branch, with `--force-with-lease`.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-42
```

Next: [Lesson 43 · Upstream branches](../43-upstream-branches/README.md).
