<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 63 · Interactive rebase · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Two quick commits to clean up, then squash the **first** line of the to-do list:

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
