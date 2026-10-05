# Module 07 · Undoing changes · Assessment

> Lessons 29–33 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-07-practical history
bash scripts/new-lab.sh assess-07-broken history
```

## Quiz

1. Which command throws away unstaged edits to `menu.txt`, and can they be recovered?
2. How do you take a file out of the next commit without losing your edit?
3. After `git reset --soft HEAD~1`, where are the changes of the removed commit?
4. What is the difference between `--mixed` and `--hard`?
5. Why use `git revert` instead of `git reset` for a commit that is on the shared `main`?
6. What does `git revert -m 1 MERGE` keep?
7. Where do you find the commit your branch pointed to before a bad `git reset --hard`?

<details>
<summary>Answers</summary>

1. `git restore menu.txt`; no, unstaged edits were never stored (lesson 29).
2. `git restore --staged FILE` (lesson 30).
3. Staged, ready to be committed again (lesson 31).
4. `--mixed` keeps the changes in the working directory (unstaged); `--hard` deletes them (lesson 31).
5. Revert adds a new commit and does not rewrite history others already have (lesson 32).
6. The first parent: the branch the merge was made on (`main`) (lesson 32).
7. `ORIG_HEAD` or `git reflog` (`HEAD@{1}`) (lesson 33).

</details>

## Practical challenge

In `~/git-practice/assess-07-practical`:

1. Combine the last two commits ("Add mocha", "Price mocha") into one commit "Add mocha with its price".
2. Undo "Price green tea" with a new commit (it is already shared). The revert conflicts with the mocha price on
   the next line: keep mocha, drop green tea's price.
3. Someone edited `README.md` by accident (simulated below): discard that edit.

<!-- test-run: cd ~/git-practice/assess-07-practical && echo "oops" >> README.md -->

<details>
<summary>Reference solution</summary>

<!-- test: contains=Add mocha with its price; output -->
```bash
cd ~/git-practice/assess-07-practical
git restore README.md
git reset -q --soft HEAD~2
git commit -q -m "Add mocha with its price"
git revert --no-edit "$(git log --format=%h -1 --grep='^Price green tea$')" > /dev/null 2>&1 || true
grep -v -e '^green tea 2.80$' -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>' -e '^|||||||' prices.txt > prices.tmp && mv prices.tmp prices.txt
git add prices.txt && git -c core.editor=true revert --continue > /dev/null
git log --oneline -4
cat prices.txt
```

```text
916e825 (HEAD -> main) Revert "Price green tea"
16de40d Add mocha with its price
269869e Price green tea
6833580 Add green tea
espresso 2.50
latte 3.20
cappuccino 3.40
mocha 3.90
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-07-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "one commit for mocha"            'git log --format=%s | grep -qx "Add mocha with its price" && ! git log --format=%s | grep -qx "Price mocha"'
check "mocha and its price present"     'grep -qx mocha menu.txt && grep -q "mocha 3.90" prices.txt'
check "green tea price reverted"        'git log --format=%s | grep -q "^Revert \"Price green tea\"" && ! grep -q "green tea 2.80" prices.txt'
check "README edit discarded, clean"    '[ -z "$(git status --porcelain)" ]'
```

```text
ok       one commit for mocha
ok       mocha and its price present
ok       green tea price reverted
ok       README edit discarded, clean
```

## Troubleshooting challenge

In `~/git-practice/assess-07-broken`, someone "cleaned up" too much:

<!-- test: contains=Add green tea; output -->
```bash
cd ~/git-practice/assess-07-broken
git reset -q --hard HEAD~3
git log --oneline -2
```

```text
6833580 (HEAD -> main) Add green tea
4267004 Add prices
```

Symptom: "Price green tea", "Add mocha" and "Price mocha" are gone, and mocha is missing from the files. Bring all
three back.

<details>
<summary>Solution</summary>

The reset moved `main`; the commits still exist. The reflog shows the position before the reset:

<!-- test: contains=Price mocha; output -->
```bash
git reflog -2
git reset --hard 'HEAD@{1}'
```

```text
6833580 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
ecff18a HEAD@{1}: commit: Price mocha
HEAD is now at ecff18a Price mocha
```

`git reset --hard ORIG_HEAD` works too, as long as nothing else moved `HEAD` since.

</details>

Verification:

<!-- test: contains=mocha 3.90; output -->
```bash
git log --oneline -3
grep mocha prices.txt
```

```text
ecff18a (HEAD -> main) Price mocha
2c389c0 Add mocha
269869e Price green tea
mocha 3.90
```

## Real-world scenario

A commit that changes the database connection string was merged to `main` an hour ago and deployed; production now
fails to connect. Two teammates have pulled `main` since. How do you undo it?

<details>
<summary>Model answer</summary>

`git revert <sha>` (or `git revert -m 1 <merge>` for a merged PR) on a branch, through a quick PR, then deploy: the
history stays intact for the teammates who pulled, and the revert is visible and auditable (lesson 32). Do not
`reset` and force-push a shared `main`. Afterwards, find the root cause and re-apply a corrected change (reverting the
revert, then fixing) in a new PR.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-07-practical ~/git-practice/assess-07-broken
```
