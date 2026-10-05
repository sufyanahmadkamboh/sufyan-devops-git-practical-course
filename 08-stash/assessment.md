# Module 08 · Stash · Assessment

> Lessons 34–36 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-08-practical basic
bash scripts/new-lab.sh assess-08-broken basic
```

## Quiz

1. What does `git stash` do with your uncommitted changes?
2. Which files does plain `git stash` leave behind, and which option includes them?
3. What is the difference between `git stash apply` and `git stash pop`?
4. `git stash pop` reports a conflict. Is the stash entry still there?
5. How do you see the full diff of the second-newest stash?
6. When is `git stash branch NAME` the better choice than `pop`?
7. Is a stash pushed with `git push`?

<details>
<summary>Answers</summary>

1. Saves them as a special commit and resets the working directory to `HEAD` (lesson 34).
2. Untracked files; `git stash -u` includes them (lesson 34).
3. `apply` keeps the entry, `pop` removes it after applying (lesson 35).
4. Yes: "The stash entry is kept in case you need it again" (lesson 35).
5. `git stash show -p 'stash@{1}'` (lesson 36).
6. When the branch moved on and the stash would conflict: it applies the stash on the commit it was made from (lesson 36).
7. No: stashes live under `refs/stash`, which is local (lesson 34).

</details>

## Practical challenge

In `~/git-practice/assess-08-practical`:

1. Make two stashes: "price draft" (latte becomes 3.30 in `prices.txt`) and "new drink" (a new file `chai.txt`).
2. Turn "price draft" into a branch `price-draft` and commit it there.
3. On `main`, restore "new drink" and commit it.
4. Leave the stash list empty.

<details>
<summary>Reference solution</summary>

<!-- test: contains=On branch price-draft; output -->
```bash
cd ~/git-practice/assess-08-practical
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git stash push -q -m "price draft"
echo "chai" > chai.txt && git stash push -q -u -m "new drink"
git stash list
git stash branch price-draft 'stash@{1}'
git commit -q -am "Raise the latte price to 3.30"
git switch -q main
git stash pop -q
git add chai.txt && git commit -q -m "Add chai"
```

```text
stash@{0}: On main: new drink
stash@{1}: On main: price draft
Switched to a new branch 'price-draft'
On branch price-draft
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped stash@{1} (b3924d85d2cba2e13685b67e0d8f7ad1b6dff6b9)
Already up to date.
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-08-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "price-draft has latte 3.30"   'git show price-draft:prices.txt | grep -qx "latte 3.30"'
check "main has chai.txt committed"  'git cat-file -e main:chai.txt'
check "main keeps latte 3.20"        'git show main:prices.txt | grep -qx "latte 3.20"'
check "stash list empty"             '[ -z "$(git stash list)" ]'
check "working tree clean"           '[ -z "$(git status --porcelain)" ]'
```

```text
ok       price-draft has latte 3.30
ok       main has chai.txt committed
ok       main keeps latte 3.20
ok       stash list empty
ok       working tree clean
```

## Troubleshooting challenge

In `~/git-practice/assess-08-broken`, a stashed price change meets a newer commit:

<!-- test: contains=Latte 3.50; output -->
```bash
cd ~/git-practice/assess-08-broken
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git stash push -q -m "latte idea"
sed -i 's/latte 3.20/latte 3.50/' prices.txt && git commit -q -am "Latte 3.50"
git log --oneline -1
```

```text
82ed6f1 (HEAD -> main) Latte 3.50
```

Symptom:

<!-- test: fail; contains=CONFLICT; output -->
```bash
git stash pop 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
On branch main
Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt

no changes added to commit (use "git add" and/or "git commit -a")
The stash entry is kept in case you need it again.
```

Resolve it (keep **3.50**, the committed decision), and leave no stash and no conflict state behind.

<details>
<summary>Solution</summary>

The pop conflicted, so the entry was kept. Take the committed version, clear the unmerged state, drop the stash:

<!-- test: contains=Dropped; output -->
```bash
git checkout --ours prices.txt
git restore --staged prices.txt
git stash drop
```

```text
Updated 1 path from the index
Dropped refs/stash@{0} (b63cf42c51f44bdd30d63aefbeb4737caef9c70a)
```

</details>

Verification:

<!-- test: contains=latte 3.50; output -->
```bash
grep latte prices.txt
git stash list | wc -l
git status --short | wc -l
```

```text
latte 3.50
0
0
```

## Real-world scenario

You have half a day of uncommitted changes when you must review and test a colleague's branch on your machine. What
do you do, and what do you avoid?

<details>
<summary>Model answer</summary>

`git stash push -u -m "WIP: <topic>"`, check out the colleague's branch (or better: `git worktree add` a second folder
so nothing needs stashing, lesson 87), test, come back, `git stash pop`. Avoid anonymous stashes and leaving work in
the stash for days: a half day of work deserves a WIP commit on your own branch, pushed, so it is backed up.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-08-practical ~/git-practice/assess-08-broken
```
