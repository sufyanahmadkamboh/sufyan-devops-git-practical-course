<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 26 · Merge conflicts · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-26 conflict
cd ~/git-practice/lesson-26
git log --oneline --graph --all
```

## Demonstration

```bash
git merge feature-tea
```

```bash
cat prices.txt
```

```bash
git checkout --conflict=diff3 prices.txt
cat prices.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-26
git diff --name-only --diff-filter=U
```

## Break it

```bash
git commit -m "Merge" 2>&1
```

## Troubleshoot

```bash
git status
```

## Fix

```bash
git merge --abort
git status
```

## Practice challenge

```bash
cd ~/git-practice/lesson-26
git config --global merge.conflictStyle zdiff3
git merge feature-tea > /dev/null 2>&1 || true
cat prices.txt
git merge --abort
```

## Cleanup

```bash
cd ~
git config --global --unset merge.conflictStyle
rm -rf ~/git-practice/lesson-26
```
