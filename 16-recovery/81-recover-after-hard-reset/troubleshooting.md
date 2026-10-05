<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 81 · Recover after a hard reset · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Work was **staged** but not committed, and a hard reset wipes it:

```bash
git reset -q --hard before-cleanup
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
git reset --hard
cat menu.txt
```

```text
HEAD is now at d37a774 Price green tea
espresso
latte
cappuccino
green tea
```

## Troubleshoot

There is no commit, so the reflog has nothing. But `git add` wrote the file's content as a **blob** into the object
store; the reset removed it from the index, leaving the blob dangling (no name, no reference):

```bash
git fsck --lost-found 2> /dev/null
```

```text
dangling blob bca981e9bc8b69d16bce2150e069815457e5b744
```

## Fix

`--lost-found` copied the dangling objects to `.git/lost-found/other/`. Find the one with your content and restore it:

```bash
for f in .git/lost-found/other/*; do
  grep -l "cortado" "$f" > /dev/null 2>&1 && cp "$f" menu.txt && echo "restored from $(basename "$f")"
done
cat menu.txt
```

```text
restored from bca981e9bc8b69d16bce2150e069815457e5b744
espresso
latte
cappuccino
green tea
flat white
cortado
```

The file name is not stored in a blob: if several files were staged, you identify them by content. Edits that were
**never staged** leave no blob at all: stage often, or commit "WIP" on a branch.
