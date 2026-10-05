<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 32 · git revert · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Revert a commit whose lines were changed again later: "Add green tea" added `green tea` to `menu.txt`, and later commits
changed that line.

```bash
sed -i 's/^green tea$/green tea (organic)/' menu.txt && git commit -q -am "Organic green tea"
git revert --no-edit "$(git log --format=%h --grep='^Add green tea')" 2>&1
```

```text
Auto-merging menu.txt
CONFLICT (content): Merge conflict in menu.txt
error: could not revert 6833580... Add green tea
hint: After resolving the conflicts, mark them with
hint: "git add/rm <pathspec>", then run
hint: "git revert --continue".
hint: You can instead skip this commit with "git revert --skip".
hint: To abort and get back to the state before "git revert",
hint: run "git revert --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
```

## Troubleshoot

A revert is a merge of the "opposite" change: if the same lines changed afterwards, it conflicts exactly like a merge
(lesson 26). `git status` says "You are currently reverting commit ...":

```bash
git status | head -4
```

```text
On branch main
You are currently reverting commit 6833580.
  (fix conflicts and run "git revert --continue")
  (use "git revert --skip" to skip this patch)
```

## Fix

Decide what the file should be (here: no green tea at all), resolve, continue:

```bash
grep -v -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>' -e 'green tea' -e '^|||||||' menu.txt > menu.tmp && mv menu.tmp menu.txt
git add menu.txt
git revert --continue > /dev/null
cat menu.txt
```

```text
espresso
latte
cappuccino
mocha
```

Or `git revert --abort` to cancel and return to the state before the revert.
