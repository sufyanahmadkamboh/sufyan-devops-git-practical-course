<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 29 · Undo working directory changes · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Restore the wrong file: a whole morning's work in `menu.txt`.

```bash
printf 'flat white\ncortado\n' >> menu.txt
git restore menu.txt
cat menu.txt
```

## Troubleshoot

The two new lines are gone, and Git cannot bring them back: they were never staged or committed, so no object was ever
written (lesson 74). Look at the reflog, the stash list, the object store: nothing.

```bash
git reflog | head -3
git stash list
git fsck --lost-found 2>/dev/null | head -3 || true
```

Your editor's undo history or local history (VS Code "Timeline", JetBrains "Local History") is the only hope.

## Fix

Prevention is the fix: anything worth keeping should be at least **staged** before you experiment. A staged version is
written as an object and survives a `restore` of the working directory:

```bash
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
echo "a bad experiment" >> menu.txt
git restore menu.txt
cat menu.txt
```

```text
espresso
latte
cappuccino
flat white
cortado
```

`git restore` restored the **staged** version: the bad experiment is gone, the two staged lines are kept.
