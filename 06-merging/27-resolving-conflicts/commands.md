<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 27 · Resolving merge conflicts · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-27 conflict
cd ~/git-practice/lesson-27
git merge feature-tea > /dev/null 2>&1 || git status --short
```

## Demonstration

```bash
cat prices.txt
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
cat prices.txt
```

```bash
git add prices.txt
git status --short
git commit -q --no-edit
git log --oneline --graph -4
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-27
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git checkout --theirs prices.txt && git add prices.txt && git commit -q --no-edit
grep latte prices.txt
```

## Break it

```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
git add prices.txt
git commit -q --no-edit
cat prices.txt
```

## Troubleshoot

```bash
git diff --check HEAD~1 HEAD 2>&1 | head -3 || true
grep -n '^<<<<<<<\|^=======\|^>>>>>>>' prices.txt
```

## Fix

```bash
git reset -q --hard HEAD~1
git merge feature-tea > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt && git commit -q --no-edit
cat prices.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-27
printf '#!/bin/sh\nexec git diff --cached --check\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
printf '<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> other\n' > test.txt && git add test.txt
git commit -m "Test" 2>&1
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-27
```
