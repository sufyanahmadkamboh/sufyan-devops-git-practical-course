<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 80 · Recover a deleted commit · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Ada pushes her work, then "starts over" on the chai commit and cleans the repository aggressively:

```bash
git push -q -u origin main
git reset -q --hard HEAD~1
git reflog expire --expire=now --all
git gc -q --prune=now
git reflog | wc -l
```

```text
0
```

## Troubleshoot

The reflog is empty and `gc --prune=now` deleted every unreachable object. Locally, the chai commit is gone:

```bash
git fsck --unreachable --no-reflogs 2> /dev/null | wc -l
git log --oneline main | grep -c chai || true
```

```text
0
0
```

Recovery inside this clone is impossible. The question becomes: **where else does this commit exist?** On the server
if it was pushed, in a colleague's clone, in CI caches, in a GitHub PR (`refs/pull/N/head`). Ada pushed it:

```bash
git log --oneline -1 origin/main
```

```text
3685547 (origin/main) Add chai and its price
```

## Fix

```bash
git reset -q --hard origin/main
git log --oneline -2
grep chai prices.txt
```

```text
3685547 (HEAD -> main, origin/main) Add chai and its price
ccd73e3 Add mocha
chai 3.10
```

Had the commit never been pushed, it would be lost for good: push work you care about, early.
