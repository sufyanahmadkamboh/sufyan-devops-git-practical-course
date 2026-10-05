<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 31 · git reset: soft, mixed and hard · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

The classic mistake: `--hard` with uncommitted work you wanted to keep.

```bash
echo "flat white 3.60" >> prices.txt
git reset --hard HEAD~1
cat prices.txt
```

## Troubleshoot

Two different things were lost:

1. **The commit** "Add green tea with its price": recoverable, it still exists as an object; the reflog knows it.
2. **The uncommitted line** "flat white 3.60": never committed or staged, so it is gone for good.

```bash
git reflog -3
```

```text
4267004 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1
6ba9a63 HEAD@{1}: commit: Add green tea with its price
4267004 (HEAD -> main) HEAD@{2}: reset: moving to HEAD~2
```

## Fix

Bring the commit back: `ORIG_HEAD` (or the reflog entry `HEAD@{1}`) is where `main` was before the reset:

```bash
git reset --hard ORIG_HEAD
git log --oneline -2
```

```text
HEAD is now at 6ba9a63 Add green tea with its price
6ba9a63 (HEAD -> main) Add green tea with its price
4267004 Add prices
```

The commit is back; the uncommitted line is not. Lesson 33 and lesson 81 go deeper into recovering after a hard reset.
