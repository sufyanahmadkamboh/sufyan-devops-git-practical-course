<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 05 · What is a Git repository? · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Run a Git command outside any repository:

```bash
mkdir -p ~/git-practice/lesson-05-plain && cd ~/git-practice/lesson-05-plain
git status 2>&1
```

```text
fatal: not a git repository (or any of the parent directories): .git
```

## Troubleshoot

`fatal: not a git repository (or any of the parent directories): .git`: Git looked for `.git` here and in every
parent folder, and found none. Either you are in the wrong folder, or the project was never initialised (or someone
deleted `.git`). Check where you are:

<!-- test -->
```bash
pwd
ls -A
```

## Fix

Go to the project folder (here, the lab):

```bash
cd ~/git-practice/lesson-05
git status
```
