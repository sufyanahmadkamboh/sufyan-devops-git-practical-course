<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 19 · Switching branches · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-19 diverged
cd ~/git-practice/lesson-19
```

## Demonstration

```bash
git status | head -1
cat menu.txt
```

```bash
git switch feature-tea
cat menu.txt
cat .git/HEAD
```

```bash
git switch main
cat menu.txt
git switch -                 # "-" = the previous branch, like cd -
git branch --show-current
git switch -q main
```

```bash
git checkout feature-tea 2>&1
git checkout main 2>&1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-19
git branch --show-current
git status --short
```

## Break it

```bash
git restore prices.txt
echo "matcha" >> menu.txt
git switch main 2>&1
```

## Troubleshoot

```bash
git branch --show-current
git status --short
```

## Fix

```bash
git commit -q -am "Add matcha"
git switch main
git branch --show-current
```

## Practice challenge

```bash
cd ~/git-practice/lesson-19
git switch --detach feature-tea 2>&1
git status | head -1
git switch -q main
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-19
```
