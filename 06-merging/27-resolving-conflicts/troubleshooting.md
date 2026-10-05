<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 27 · Resolving merge conflicts · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Resolve carelessly: "resolve" by staging the file with the markers still in it.

```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git add prices.txt
git commit -q --no-edit
cat prices.txt
```

## Troubleshoot

Git accepted it: `git add` means "resolved" whatever the content. The markers are now **committed**, and anything that
reads `prices.txt` breaks. Find committed markers before they spread:

```bash
git diff --check HEAD~1 HEAD 2>&1 | head -3 || true
grep -n '^<<<<<<<\|^=======\|^>>>>>>>' prices.txt
```

`git diff --check` reports "leftover conflict marker".

## Fix

The merge is not pushed: redo it properly. Undo the bad merge commit, merge again, resolve for real:

```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q --no-edit
cat prices.txt
```

```text
espresso 2.50
latte 3.40
cappuccino 3.40
```
