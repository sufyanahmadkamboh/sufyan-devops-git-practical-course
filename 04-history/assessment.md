# Module 04 · Git history · Assessment

> Lessons 13–16 · ⏱ 30 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-04-history history
bash scripts/new-lab.sh assess-04-broken basic
```

## Quiz

1. Which command shows the history as one line per commit?
2. How do you list only the commits that changed `prices.txt`?
3. Which option finds commits that added or removed a given text?
4. What does `git show COMMIT:FILE` print?
5. `git diff` shows nothing, but you know you changed a file. What is the most likely reason?
6. What is the difference between `git diff A B` and `git diff A...B`?
7. Which options draw the branch graph with all branches?

<details>
<summary>Answers</summary>

1. `git log --oneline` (lesson 13).
2. `git log -- prices.txt` (lesson 13).
3. `git log -S "TEXT"` (lesson 13).
4. The file's content as it was in that commit (lesson 14).
5. The change is staged; `git diff` shows only unstaged changes, `git diff --cached` shows staged ones (lesson 15).
6. Two dots: the difference between the two snapshots; three dots: B's changes since its merge base with A (lesson 15).
7. `git log --oneline --graph --all` (lesson 16).

</details>

## Practical challenge

In `assess-04-history`, answer with Git commands: (1) which commit introduced the mocha price, (2) what `prices.txt`
looked like in the commit "Add prices", (3) how many commits touched `menu.txt`.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Price mocha; contains=latte 3.20; output -->
```bash
cd ~/git-practice/assess-04-history
git log --oneline -S "mocha 3.90"
git show 4267004:prices.txt
git log --oneline -- menu.txt | wc -l
```

```text
ecff18a (HEAD -> main) Price mocha
espresso 2.50
latte 3.20
cappuccino 3.40
3
```

</details>

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-04-history
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "mocha price came in 'Price mocha'" '[ "$(git log --format=%s -S "mocha 3.90")" = "Price mocha" ]'
check "Add prices had 3 price lines"     '[ "$(git show 4267004:prices.txt | wc -l)" -eq 3 ]'
check "3 commits touched menu.txt"       '[ "$(git log --oneline -- menu.txt | wc -l)" -eq 3 ]'
```

```text
ok       mocha price came in 'Price mocha'
ok       Add prices had 3 price lines
ok       3 commits touched menu.txt
```

## Troubleshooting challenge

In `assess-04-broken`, a colleague changed the latte price and says "`git diff` is broken, it shows nothing":

<!-- test: contains=lab -->
```bash
cd ~/git-practice/assess-04-broken
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git add prices.txt
echo "lab: change staged"
```

Symptom:

<!-- test: output -->
```bash
git diff | wc -l
git status --short
```

```text
0
M  prices.txt
```

<details>
<summary>Solution</summary>

`M ` in the first column: the change is staged. `git diff` compares the working directory with the staging area,
where the file is identical. Compare the staging area with the last commit instead:

<!-- test: contains=+latte 3.30; output -->
```bash
git diff --cached
```

```text
diff --git a/prices.txt b/prices.txt
index 5813ff5..ddaed76 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,3 @@
 espresso 2.50
-latte 3.20
+latte 3.30
 cappuccino 3.40
```

</details>

## Real-world scenario

Production started charging a wrong price yesterday. The prices live in a Git repository with 200 commits from five
people. Which commands get you from "something changed" to "this commit, by this person, for this reason" quickly?

<details>
<summary>Model answer</summary>

`git log --oneline --since=yesterday -- prices.txt` narrows the commits; `git log -p -S "latte 3." -- prices.txt`
finds the exact change of the price text; `git show SHA` shows the full commit with author and message, which should
explain why. `git blame -L` on the line (lesson 71) and `git diff GOOD BAD -- prices.txt` between the last good and the
current version confirm it. Then fix forward with a new commit or revert (lesson 32).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-04-history ~/git-practice/assess-04-broken
```
