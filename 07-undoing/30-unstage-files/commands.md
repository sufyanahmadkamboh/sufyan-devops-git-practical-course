<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 30 · Unstage files · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-30 basic
cd ~/git-practice/lesson-30
```

## Demonstration

```bash
echo "mocha" >> menu.txt
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add .
git status --short
```

```bash
git restore --staged prices.txt
git status --short
git diff prices.txt
```

```bash
git commit -m "Add mocha"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-30
git status --short
```

## Break it

```bash
mkdir -p ~/git-practice/lesson-30-new && cd ~/git-practice/lesson-30-new && git init -q
echo hello > hello.txt && git add hello.txt
git restore --staged hello.txt 2>&1
```

## Troubleshoot

```bash
cd ~/git-practice/lesson-30-new
git status | grep -A1 "Changes to be committed"
```

## Fix

```bash
git rm -q --cached hello.txt
git status --short
cd ~/git-practice/lesson-30
```

## Practice challenge

```bash
cd ~/git-practice/lesson-30
git add .
git restore --staged .
git status --short
git diff --stat
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-30 ~/git-practice/lesson-30-new
```
