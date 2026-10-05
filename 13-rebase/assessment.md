# Module 13 · Rebase · Assessment

> Lessons 60–66 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

A history to clean up, and a repository left in the middle of a rebase:

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh assess-13-rebase history
bash scripts/new-lab.sh assess-13-broken conflict
(cd ~/git-practice/assess-13-rebase && git switch -q -c feature-notes 4267004 &&
  echo "Ask about oat milk." > notes.txt && git add notes.txt && git commit -q -m "Add notes" && git switch -q main)
(cd ~/git-practice/assess-13-broken && git switch -q feature-tea &&
  echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && (git rebase main > /dev/null 2>&1 || true))
```

## Quiz

1. After `git rebase main`, your branch's commits have new IDs. Why?
2. State the golden rule of rebasing.
3. Your rebased feature branch is rejected on push. Which push command is the safe way to update it, and why not
   `--force`?
4. In an interactive rebase, what is the difference between `squash` and `fixup`?
5. During a rebase conflict, which side is "ours" and which is "theirs"?
6. You resolved a conflict and ran `git rebase --continue`; Git says to "mark them as resolved using git add". What
   did you forget?
7. Which command returns everything to the state before a rebase started?
8. At an `edit` stop you run `git commit -am "…"` instead of `git commit --amend`. What happens?

<details>
<summary>Answers</summary>

1. Each commit is replayed onto a new parent; the parent is part of the content that is hashed (lesson 60).
2. Never rebase commits others have built on (60, 62).
3. `git push --force-with-lease`: it refuses if someone else pushed to the branch since your last fetch (60).
4. Both meld the commit into the previous one; `squash` combines the messages, `fixup` keeps only the previous one (63).
5. "Ours" is the branch you are rebasing onto (e.g. `main`); "theirs" is your commit being replayed (64).
6. `git add FILE` to mark the conflict resolved (64).
7. `git rebase --abort` (65).
8. A new, extra commit is added after the stopped one instead of changing it (66).

</details>

## Practical challenge

In `~/git-practice/assess-13-rebase`:

1. Rewrite the last four commits of `main` into **two**: "Add green tea" must include its price (fold "Price green
   tea" into it without keeping its message), and "Add mocha" together with "Price mocha" becomes one commit named
   `Add mocha with its price`.
2. Rebase `feature-notes` onto the new `main`; it must not contain merge commits.

<details>
<summary>Reference solution</summary>

<!-- test: contains=Add mocha with its price; output -->
```bash
cd ~/git-practice/assess-13-rebase
GIT_SEQUENCE_EDITOR="sed -i -e '2s/^pick/fixup/' -e '3s/^pick/reword/' -e '4s/^pick/fixup/'" \
  GIT_EDITOR="sed -i '1s/.*/Add mocha with its price/'" git rebase -q -i HEAD~4
git switch -q feature-notes && git rebase -q main && git switch -q main
git log --oneline --graph --all -5
```

```text
[detached HEAD 7636225] Add mocha with its price
 Date: Mon Jan 5 09:06:00 2026 +0000
 1 file changed, 1 insertion(+)
* e725308 (feature-notes) Add notes
* 49596ee (HEAD -> main) Add mocha with its price
* fe9c683 Add green tea
* 4267004 Add prices
* fc345e6 Add the menu
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-13-rebase
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "two commits after 'Add prices'"         '[ "$(git rev-list --count 4267004..main)" -eq 2 ]'
check "'Add green tea' includes its price"     'git show --stat "$(git log --format=%h -1 --grep="^Add green tea$" main)" | grep -q prices.txt'
check "'Add mocha with its price' exists"      '[ "$(git log -1 --format=%s main)" = "Add mocha with its price" ]'
check "no 'Price …' messages left on main"     '! git log --format=%s main | grep -q "^Price"'
check "feature-notes is on top of main"        'git merge-base --is-ancestor main feature-notes'
check "feature-notes has no merge commits"     '[ "$(git rev-list --merges --count main..feature-notes)" -eq 0 ]'
```

```text
ok       two commits after 'Add prices'
ok       'Add green tea' includes its price
ok       'Add mocha with its price' exists
ok       no 'Price …' messages left on main
ok       feature-notes is on top of main
ok       feature-notes has no merge commits
```

## Troubleshooting challenge

A colleague started `git rebase main` on `feature-tea` in `~/git-practice/assess-13-broken`, then went home. Now
nothing works:

<!-- test: fail; contains=while rebasing; output -->
```bash
cd ~/git-practice/assess-13-broken
git switch main 2>&1
```

```text
fatal: cannot switch branch while rebasing
Consider "git rebase --quit" or "git worktree add".
```

Finish the rebase. The agreed latte price is **3.40**, and the branch must keep its green tea commit.

<details>
<summary>Solution</summary>

Read the state first (lesson 64):

<!-- test: contains=rebase in progress; output -->
```bash
git status | head -6
```

```text
interactive rebase in progress; onto 594657b
Last command done (1 command done):
   pick 00931cc # Raise the latte price to 3.50
Next command to do (1 remaining command):
   pick 8b2d817 # Add green tea
  (use "git rebase --edit-todo" to view and edit)
```

Resolve the current commit, mark it, continue (the green tea commit replays without conflict):

<!-- test: contains=Successfully rebased; output -->
```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git rebase --continue 2>&1 | tail -1
```

```text
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-tea.
```

</details>

Verification:

<!-- test: contains=Add green tea; output -->
```bash
cd ~/git-practice/assess-13-broken
git status | head -2
git log --oneline -3
grep latte prices.txt
```

```text
On branch feature-tea
nothing to commit, working tree clean
be16bfa (HEAD -> feature-tea) Add green tea
bc27de7 Raise the latte price to 3.50
594657b (main) Raise the latte price to 3.30
latte 3.40
```

## Real-world scenario

Your PR branch has 23 commits ("wip", "fix", "address review", "oops") and is 40 commits behind `main`. The reviewer
asks for a clean, up-to-date branch before merging. Two colleagues have checked out your branch to test it.

<details>
<summary>Model answer</summary>

Tell the two colleagues first, because rewriting a branch they have pulled affects them. Then squash locally with
`git rebase -i origin/main` (fixup the noise into a few meaningful commits), resolving conflicts once per remaining
commit, or enable `rerere`. Run the tests, push with `git push --force-with-lease`, and ask the colleagues to
`git fetch && git reset --hard origin/BRANCH` (or `git pull --rebase`) rather than merging the old version back in.
If others had committed on the branch, prefer merging `main` into it instead of rebasing.

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-13-rebase ~/git-practice/assess-13-broken
```
