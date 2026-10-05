<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 09 · git add · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Stage a file that should never be committed (a local secret) with a careless `git add .`:

```bash
echo "DB_PASSWORD=example-only-not-a-real-secret" > .env
git add .
git status --short
```

## Troubleshoot

`A  .env`: the secrets file is staged. It is **not committed yet**: the staging area is a draft, and you can take
things out of it before the commit. That is the moment to look at `git status` before every commit.

## Fix

Unstage it (lesson 30 covers `git restore --staged`), and make Git ignore it from now on (lesson 73):

```bash
git restore --staged .env
echo ".env" > .gitignore
git add .gitignore
git status --short
```

```text
A  .gitignore
M  menu.txt
A  notes.txt
M  prices.txt
```

`.env` disappeared from the list entirely: it is ignored, so `git add .` will never pick it up again.
