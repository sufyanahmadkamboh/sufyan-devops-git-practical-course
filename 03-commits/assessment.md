# Module 03 · Commits · Assessment

> Lessons 09–12 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-03-split basic
bash scripts/new-lab.sh assess-03-broken basic
```

## Quiz

1. What does `git add` do to a file?
2. Why does Git have a staging area at all?
3. Which command stages only some of the changes inside one file?
4. What does a commit object contain?
5. Why does `git commit --amend` change the commit ID?
6. When is amending a commit unsafe?
7. What does `git commit -a` include, and what does it skip?
8. Write a good commit subject for "changed the latte price from 3.20 to 3.30".

<details>
<summary>Answers</summary>

1. It copies the file's current content into the staging area for the next commit (lesson 09).
2. To build each commit deliberately: choose exactly which changes belong together (lesson 10).
3. `git add -p FILE` (lesson 10).
4. A tree (the snapshot), parent(s), author, committer, dates and the message (lesson 12).
5. The ID is a hash of the commit's content; new message or content means a new hash (lesson 12).
6. When the commit was already pushed and others may have it (lesson 12).
7. Modified and deleted tracked files; new untracked files are skipped (lesson 11).
8. Something like `Raise the latte price to 3.30` (imperative, specific, short) (lesson 11).

</details>

## Practical challenge

In `assess-03-split`, add `chai` to `menu.txt` and change the espresso price to 2.60 in `prices.txt`. Record them as
**two** commits: "Add chai to the menu" and "Raise the espresso price to 2.60", in that order.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Raise the espresso price to 2.60; output -->
```bash
cd ~/git-practice/assess-03-split
echo "chai" >> menu.txt
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt
git add menu.txt && git commit -q -m "Add chai to the menu"
git add prices.txt && git commit -q -m "Raise the espresso price to 2.60"
git log --oneline -3
```

```text
6dc55b2 (HEAD -> main) Raise the espresso price to 2.60
e0f45a2 Add chai to the menu
4267004 Add prices
```

</details>

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-03-split
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "last commit only touches prices.txt" '[ "$(git show --name-only --format= HEAD)" = prices.txt ]'
check "previous commit only touches menu.txt" '[ "$(git show --name-only --format= HEAD~1)" = menu.txt ]'
check "messages in the right order" '[ "$(git log -1 --format=%s HEAD~1)" = "Add chai to the menu" ]'
check "nothing left uncommitted" '[ -z "$(git status --porcelain)" ]'
```

```text
ok       last commit only touches prices.txt
ok       previous commit only touches menu.txt
ok       messages in the right order
ok       nothing left uncommitted
```

## Troubleshooting challenge

In `assess-03-broken`, a commit was made with a typo in the message, and a file that belonged to it was forgotten:

<!-- test: contains=prcie -->
```bash
cd ~/git-practice/assess-03-broken
echo "mocha" >> menu.txt && echo "mocha 3.90" >> prices.txt
git add menu.txt && git commit -q -m "Add mocha and its prcie"
git log --oneline -1
```

Symptom:

<!-- test: contains= M prices.txt; output -->
```bash
git show --stat --format=%s HEAD
git status --short
```

```text
Add mocha and its prcie

 menu.txt | 1 +
 1 file changed, 1 insertion(+)
 M prices.txt
```

<details>
<summary>Solution</summary>

The commit is not pushed, so amend it: stage the forgotten file and fix the message in one step.

<!-- test: contains=Add mocha and its price; output -->
```bash
git add prices.txt
git commit -q --amend -m "Add mocha and its price"
git show --stat --format=%s HEAD
git status --short | wc -l
```

```text
Add mocha and its price

 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
0
```

</details>

## Real-world scenario

A pull request contains one commit "fixes" that changes the Helm chart, a Terraform variable and a typo in the README.
The reviewer asks you to split it. Why does that matter, and how would you have avoided it?

<details>
<summary>Model answer</summary>

Small, single-purpose commits can be reviewed, reverted and cherry-picked independently, and their messages explain
the history (`git log`, `git blame`). Avoid mixed commits by staging deliberately: `git add FILE` or `git add -p` per
purpose, checking `git diff --cached` before each commit, and writing a specific message. To split an existing
commit: `git reset HEAD~1` (keeps the changes) and commit again in pieces (lessons 10, 31).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-03-split ~/git-practice/assess-03-broken
```
