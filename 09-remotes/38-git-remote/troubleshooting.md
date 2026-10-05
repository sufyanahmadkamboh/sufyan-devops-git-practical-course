<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 38 · git remote · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Add `origin` again, as you would after copying a "connect this repository" snippet from GitHub:

```bash
git remote add origin ../server/cafe-shop.git 2>&1
```

```text
error: remote origin already exists.
```

## Troubleshoot

`error: remote origin already exists.`: a clone already has `origin`. The snippet assumes a fresh `git init`. Check what
`origin` currently is before deciding:

```bash
git remote get-url origin
```

## Fix

If the URL is what you wanted, there is nothing to do. If not, change it (`set-url`), never add a second `origin`:

```bash
git remote set-url origin ../server/cafe-shop.git
git remote -v
```
