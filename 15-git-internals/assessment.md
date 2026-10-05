# Module 15 · Git internals · Assessment

> Lessons 74–78 · ⏱ 40 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-15-int basic
bash scripts/new-lab.sh assess-15-broken history
(cd ~/git-practice/assess-15-broken && git switch -q --detach 4267004 &&
  sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix: espresso price" &&
  git switch -q main 2> /dev/null && echo "ref: refs/heads/mian" > .git/HEAD)
```

## Quiz

1. Name Git's four object types and what each stores.
2. Why do two files with identical content share one blob, even under different names?
3. What does `git cat-file -p HEAD` show, and which line connects a commit to its files?
4. Which plumbing commands does `git commit` correspond to?
5. What does `.git/HEAD` normally contain, and what does it contain in detached HEAD?
6. A branch is "deleted". What exactly was removed, and what still exists?
7. You made a commit in detached HEAD and switched to `main`. How do you get it back?
8. How does Git notice that an object file on disk was corrupted?

<details>
<summary>Answers</summary>

1. Blob (file content), tree (folder: names → blobs/trees), commit (tree, parents, author, message), tag (annotated
   tag) (lesson 74).
2. An object's ID is the hash of its content; names live in trees (74).
3. The commit object; the `tree` line points to the snapshot (74, 75).
4. `write-tree`, `commit-tree`, `update-ref` (after `hash-object`/`update-index` for `git add`) (75).
5. `ref: refs/heads/BRANCH`; detached: a commit ID (76, 78).
6. The reference (a name → ID); the commits remain until garbage collection (77).
7. Find it in `git reflog` and create a branch on it: `git branch NAME SHA` (78).
8. Every object is verified against its hash when read; `git fsck` checks them all (74).

</details>

## Practical challenge

In `~/git-practice/assess-15-int`, using plumbing commands only for steps 2 and 3:

1. Show that the blob of `prices.txt` at `HEAD` has the same ID as `git hash-object prices.txt`.
2. Create a branch `experiment` pointing at "Add the menu" (`fc345e6`) without `git branch`.
3. Add `chai` to `menu.txt` and create the commit "Add chai (plumbing)" on `main` without `git add` or `git commit`;
   afterwards `git status` must be clean.

<details>
<summary>Reference solution</summary>

<!-- test: contains=same blob; output -->
```bash
cd ~/git-practice/assess-15-int
[ "$(git rev-parse HEAD:prices.txt)" = "$(git hash-object prices.txt)" ] && echo "same blob"
git update-ref refs/heads/experiment fc345e6
echo "chai" >> menu.txt
git update-index menu.txt
tree=$(git write-tree)
commit=$(echo "Add chai (plumbing)" | git commit-tree "$tree" -p main)
git update-ref refs/heads/main "$commit"
git log --oneline -2
```

```text
same blob
f26e064 (HEAD -> main) Add chai (plumbing)
4267004 Add prices
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-15-int
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "experiment points at fc345e6"          '[ "$(git rev-parse experiment)" = "$(git rev-parse fc345e6)" ]'
check "main's last commit is the plumbing one" '[ "$(git log -1 --format=%s main)" = "Add chai (plumbing)" ]'
check "chai is in the commit"                  'git show main:menu.txt | grep -q chai'
check "parent is 'Add prices'"                 '[ "$(git rev-parse main~1)" = "$(git rev-parse 4267004)" ]'
check "working tree clean"                     '[ -z "$(git status --porcelain)" ]'
```

```text
ok       experiment points at fc345e6
ok       main's last commit is the plumbing one
ok       chai is in the commit
ok       parent is 'Add prices'
ok       working tree clean
```

## Troubleshooting challenge

In `~/git-practice/assess-15-broken`, a script went wrong. `git status` claims the repository is empty, and a colleague
says their espresso hotfix "was committed this morning" but is on no branch.

<!-- test: contains=No commits yet; output -->
```bash
cd ~/git-practice/assess-15-broken
git status 2>&1 | head -3
```

```text
On branch mian

No commits yet
```

Repair `HEAD` and save the hotfix on a branch `hotfix-espresso`.

<details>
<summary>Solution</summary>

`HEAD` names a branch that does not exist (lesson 76); the branches themselves are fine:

<!-- test: contains=ref: refs/heads/mian; output -->
```bash
cat .git/HEAD
git branch
```

```text
ref: refs/heads/mian
  main
```

<!-- test: contains=Hotfix: espresso price; output -->
```bash
git symbolic-ref HEAD refs/heads/main
git reflog | grep -m1 "Hotfix"
git branch hotfix-espresso "$(git reflog --format=%h --grep-reflog='commit: Hotfix' | head -1)"
git log --oneline -1 hotfix-espresso
```

```text
8911c97 HEAD@{2}: commit: Hotfix: espresso price
8911c97 (hotfix-espresso) Hotfix: espresso price
```

</details>

Verification:

<!-- test: contains=espresso 2.45; output -->
```bash
cd ~/git-practice/assess-15-broken
git status | head -1
git show hotfix-espresso:prices.txt | head -1
```

```text
On branch main
espresso 2.45
```

## Real-world scenario

`git status` on a build server prints `fatal: bad object HEAD` after the disk filled up during a fetch. The repository
is a clone of GitHub; nothing on the server was committed locally.

<details>
<summary>Model answer</summary>

Run `git fsck --full` to see which objects are missing or corrupt. Because nothing exists only in this clone, the
safest fix is to delete the working copy and clone again (or `git fetch` into a fresh clone); corrupt objects cannot
be repaired, only replaced from another copy. If local work did exist, copy the working tree aside first, then recover
missing objects by fetching from the remote. Free disk space and add monitoring so builds fail early.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-15-int ~/git-practice/assess-15-broken
```
