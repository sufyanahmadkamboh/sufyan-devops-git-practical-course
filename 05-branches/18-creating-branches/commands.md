<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 18 · Creating branches · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-18 basic
cd ~/git-practice/lesson-18
```

## Demonstration

```bash
git branch
```

```bash
git branch feature-login
git branch
git log --oneline -1
```

```bash
cat .git/refs/heads/feature-login
git rev-parse main
```

```bash
git branch hotfix-prices HEAD~1
git branch -v
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-18
git branch
```

## Break it

```bash
git branch hotfix-prices 2>&1
```

```bash
git branch "fix prices" 2>&1
```

## Troubleshoot

```bash
git check-ref-format --branch "fix-prices"
```

## Fix

```bash
git branch fix-prices
git branch
```

## Practice challenge

```bash
cd ~/git-practice/lesson-18
git branch before-prices "$(git log --format=%h --grep='Add the menu')"
git branch -v
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-18
```
