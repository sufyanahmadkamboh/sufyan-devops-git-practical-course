<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 76 · HEAD · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Edit `.git/HEAD` to point to a branch that does not exist (as a broken script or typo would):

```bash
echo "ref: refs/heads/mian" > .git/HEAD
git status 2>&1 | head -3
```

```text
On branch mian

No commits yet
```

## Troubleshoot

`On branch mian … No commits yet`: Git believes you are on a brand-new, empty branch, because `HEAD` names a branch
that has no commit. Nothing is lost: your branches are untouched.

```bash
git branch
```

```text
  feature-tea
  main
```

## Fix

Point `HEAD` back to a real branch (the safe way, with the command instead of editing the file):

```bash
git symbolic-ref HEAD refs/heads/feature-tea
git symbolic-ref HEAD
git status --short | wc -l
```
