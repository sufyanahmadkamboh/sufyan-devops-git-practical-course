# Lesson 63 · Interactive rebase

> Level 13 · Rebase · ⏱ 30 minutes

## What are we learning?

`git rebase -i` opens a to-do list of your commits, one per line, and lets you decide what happens to each: keep, edit
the message, stop to change it, combine, or delete. It is how you turn a messy work-in-progress branch into a clean
series of commits before review.

## Visual

```text
 git rebase -i HEAD~4  opens your editor with:

 pick 6833580 Add green tea          pick   keep as is
 pick 269869e Price green tea        reword keep, but edit the message
 pick 2c389c0 Add mocha              edit   stop after applying it (amend, split …)
 pick ecff18a Price mocha            squash meld into the previous commit, combine messages
                                     fixup  meld into the previous commit, discard this message
                                     drop   remove the commit
 save and close → Git replays the list from top (oldest) to bottom (newest)
```

In this course the editor is replaced by a command (`GIT_SEQUENCE_EDITOR`), so every step can be run and checked; in
your terminal you edit the words in the file and save.

## Lab setup

<!-- test: contains=lesson-63 -->
```bash
bash scripts/new-lab.sh lesson-63 history
cd ~/git-practice/lesson-63
git log --oneline
```

## Demonstration

See the to-do list Git would open (`cat` as the "editor" prints it and changes nothing):

<!-- test: contains=pick 6833580; output=head:6 -->
```bash
GIT_SEQUENCE_EDITOR=cat git rebase -i HEAD~4
```

```text
pick 6833580 # Add green tea
pick 269869e # Price green tea
pick 2c389c0 # Add mocha
pick ecff18a # Price mocha

# Rebase 4267004..ecff18a onto 4267004 (4 commands)
...
```

**squash** "Price green tea" into "Add green tea", and **fixup** "Price mocha" into "Add mocha":

<!-- test: contains=Add mocha; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i -e '2s/^pick/squash/' -e '4s/^pick/fixup/'" git rebase -q -i HEAD~4
git log --oneline -3
git show --stat --format='%s%n%b' HEAD~1
```

```text
[detached HEAD f1ec0f5] Add green tea
 Date: Mon Jan 5 09:04:00 2026 +0000
 2 files changed, 2 insertions(+)
7ae9ff5 (HEAD -> main) Add mocha
f1ec0f5 Add green tea
4267004 Add prices
Add green tea
Price green tea


 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
```

Four commits became two. The squashed commit's message combines both messages (you would edit it in the editor;
here `GIT_EDITOR=true` keeps it as proposed). **reword** the last one:

<!-- test: contains=Add mocha with its price; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/reword/'" GIT_EDITOR="sed -i '1s/.*/Add mocha with its price/'" git rebase -q -i HEAD~2
git log --oneline -3
```

```text
[detached HEAD e75c379] Add mocha with its price
 Date: Mon Jan 5 09:06:00 2026 +0000
 2 files changed, 2 insertions(+)
e75c379 (HEAD -> main) Add mocha with its price
f1ec0f5 Add green tea
4267004 Add prices
```

## Command breakdown

| To-do command | Effect |
|---|---|
| `pick` (`p`) | use the commit |
| `reword` (`r`) | use it, edit the message |
| `edit` (`e`) | use it, stop for amending (lesson 66) |
| `squash` (`s`) | meld into the previous commit, edit the combined message |
| `fixup` (`f`) | meld into the previous commit, keep the previous message |
| `drop` (`d`) or delete the line | remove the commit |
| reorder lines | reorder commits |
| `git commit --fixup=SHA` + `git rebase -i --autosquash` | mark a fix for an older commit, squash it automatically |

## Hands-on exercise

**Instructions.** `drop` the commit "Add mocha with its price" from the history.

**Expected result.** No mocha in `menu.txt` or `prices.txt`; the green tea commit is the newest.

<!-- test-run: cd ~/git-practice/lesson-63 && GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/drop/'" git rebase -q -i HEAD~2 -->

**Verification.**

<!-- test: absent=mocha -->
```bash
cd ~/git-practice/lesson-63
cat menu.txt prices.txt
git log --oneline -2
```

## Break it

Two quick commits to clean up, then squash the **first** line of the to-do list:

<!-- test: fail; contains=cannot 'squash' without a previous commit; output -->
```bash
echo "chai" >> menu.txt && git commit -q -am "WIP chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "fix: forgot the price"
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/squash/'" git rebase -i HEAD~1 2>&1
```

```text
error: cannot 'squash' without a previous commit
You can fix this with 'git rebase --edit-todo' and then run 'git rebase --continue'.
Or you can abort the rebase with 'git rebase --abort'.
```

## Troubleshoot

`cannot 'squash' without a previous commit`: squash and fixup meld a commit into the one **above** it in the list; the
first line has nothing above it. Git refuses the list before doing anything: the rebase is in progress with "No
commands done". Fix the list with `git rebase --edit-todo` (then `git rebase --continue`), or abort:

<!-- test: contains=No commands done; output -->
```bash
git status | head -2
git rebase --abort 2>&1 || true
```

```text
interactive rebase in progress; onto 75ebc70
No commands done.
```

## Fix

Include the commit to meld into: `HEAD~2`, and `fixup` the **second** line; then give the result a proper message.

<!-- test: contains=Add chai with its price; output -->
```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/fixup/'" git rebase -q -i HEAD~2
git commit -q --amend -m "Add chai with its price"
git log --oneline -3
git show --stat --format=%s HEAD | tail -3
```

```text
29c15a2 (HEAD -> main) Add chai with its price
f1ec0f5 Add green tea
4267004 Add prices
 menu.txt   | 1 +
 prices.txt | 1 +
 2 files changed, 2 insertions(+)
```

## Real-world example

A typical branch before review: "WIP", "fix typo", "really fix it", "address review", "oops". `git rebase -i
origin/main` turns it into "Add the payment webhook handler" + "Document the webhook secret rotation". During review,
`git commit --fixup=<sha>` records each fix against the right commit, and `git rebase -i --autosquash origin/main` folds
them in before merging.

## Practice challenge

Use `--fixup` and `--autosquash`: change the espresso price, commit it as a fixup of "Add prices", and fold it in.

<details>
<summary>Solution</summary>

<!-- test: contains=espresso 2.60; output -->
```bash
cd ~/git-practice/lesson-63
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt
git commit -q -a --fixup=4267004
git log --oneline -1
GIT_SEQUENCE_EDITOR=true git rebase -q -i --autosquash fc345e6
git log --oneline
git show ':/^Add prices' | grep "^+espresso"
```

```text
2cc5415 (HEAD -> main) fixup! Add prices
0006fb5 (HEAD -> main) Add chai with its price
cb5bae3 Add green tea
825cce0 Add prices
fc345e6 Add the menu
d6df412 Add README
+espresso 2.60
```

`--fixup` creates a commit named `fixup! Add prices`; `--autosquash` moves it right below "Add prices" and turns it
into `fixup`. The rebase must start **before** "Add prices" (at `fc345e6`, "Add the menu"), so it is included; the
later commits get new IDs because their parent changed.

</details>

## Recap

- `git rebase -i BASE` lists the commits after BASE; edit the verbs, save, Git replays.
- pick, reword, edit, squash, fixup, drop; reorder by moving lines.
- Only on commits you have not shared (or your own branch, then `--force-with-lease`).

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-63
```

Next: [Lesson 64 · Rebase conflicts](../64-rebase-conflicts/README.md).
