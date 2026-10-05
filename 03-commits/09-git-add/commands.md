<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 09 · git add · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-09 basic
cd ~/git-practice/lesson-09
```

## Demonstration

```bash
echo "green tea" >> menu.txt
sed -i 's/latte 3.20/latte 3.30/' prices.txt
echo "Ideas for next season" > notes.txt
git status --short
```

```bash
git add menu.txt
git status --short
```

```bash
git add .
git status --short
```

```bash
echo "chai" >> menu.txt
git status --short
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-09
git add -n .
git status --short
```

## Break it

```bash
echo "DB_PASSWORD=example-only-not-a-real-secret" > .env
git add .
git status --short
```

## Fix

```bash
git restore --staged .env
echo ".env" > .gitignore
git add .gitignore
git status --short
```

## Practice challenge

```bash
cd ~/git-practice/lesson-09
git add -A && git commit -q -m "Save the lesson's changes"
mkdir -p docs && echo "a" > docs/a.md && echo "b" > docs/b.md && echo "x" >> README.md
cd docs
git add .
git status --short
echo "---"
git add -A
git status --short
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-09
```
