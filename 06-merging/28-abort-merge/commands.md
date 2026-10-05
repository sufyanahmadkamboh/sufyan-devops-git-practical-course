<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 28 · Aborting a merge · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-28 conflict
cd ~/git-practice/lesson-28
```

## Demonstration

```bash
git merge feature-tea 2>&1
```

```bash
ls .git/MERGE_HEAD
git merge --abort
git status
ls .git/MERGE_HEAD 2>&1 || true
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-28
grep latte prices.txt
```

## Break it

```bash
echo "draft" >> prices.txt
git merge feature-tea 2>&1
```

## Fix

```bash
git stash -q
git merge feature-tea > /dev/null 2>&1 || git merge --abort
git stash pop -q
tail -1 prices.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-28
git restore prices.txt
git merge feature-tea > /dev/null 2>&1 || true
git rev-parse -q --verify MERGE_HEAD > /dev/null && echo "merge in progress" || echo "no merge"
git merge --abort
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-28
```
