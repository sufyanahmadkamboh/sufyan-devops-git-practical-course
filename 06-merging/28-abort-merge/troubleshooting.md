<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 28 · Aborting a merge · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Start a merge with **uncommitted work** in your folder. Git refuses for files the merge would touch; for others it
merges, and then an abort could mix things up. Here: uncommitted work in a file the merge touches.

```bash
echo "draft" >> prices.txt
git merge feature-tea 2>&1
```

```text
error: Your local changes to the following files would be overwritten by merge:
	prices.txt
Please commit your changes or stash them before you merge.
Aborting
Merge with strategy ort failed.
```

## Troubleshoot

`Your local changes to the following files would be overwritten by merge`: Git refuses to start, protecting your
uncommitted edit. Nothing was merged; there is nothing to abort. The rule: start merges from a clean working
directory, so that `--abort` can always restore everything.

## Fix

Put the draft aside (lesson 35, `git stash`), merge, abort if needed, bring the draft back:

```bash
git stash -q
git merge feature-tea > /dev/null 2>&1 || git merge --abort
git stash pop -q
tail -1 prices.txt
```

```text
draft
```
