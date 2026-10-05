<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 05 · What is a Git repository? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-05 basic
cd ~/git-practice/lesson-05
```

## Demonstration

```bash
ls -A
```

```bash
ls -F .git
```

```bash
cat .git/HEAD
cat .git/refs/heads/main
git log --oneline -1
```

```bash
git count-objects -v | head -2
find .git/objects -type f | head -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-05
mkdir -p docs/notes && cd docs/notes
git rev-parse --show-toplevel --git-dir
```

## Break it

```bash
mkdir -p ~/git-practice/lesson-05-plain && cd ~/git-practice/lesson-05-plain
git status 2>&1
```

## Troubleshoot

```bash
pwd
ls -A
```

## Fix

```bash
cd ~/git-practice/lesson-05
git status
```

## Practice challenge

```bash
cd ~/git-practice/lesson-05
ref=$(sed 's/ref: //' .git/HEAD)
id=$(cat ".git/$ref")
git cat-file -p "$id"
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-05 ~/git-practice/lesson-05-plain
```
