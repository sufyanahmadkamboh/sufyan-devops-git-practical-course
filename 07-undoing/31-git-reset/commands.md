<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 31 · git reset: soft, mixed and hard · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-31 history
cd ~/git-practice/lesson-31
git log --oneline
```

## Demonstration

```bash
git reset --soft HEAD~1
git log --oneline -1
git status --short
```

```bash
git commit -q -m "Add the mocha price"
git log --oneline -1
```

```bash
git reset HEAD~1
git status --short
```

```bash
git reset --hard HEAD~1
git log --oneline -1
git status
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-31
git show --stat --format=%s HEAD
```

## Break it

```bash
echo "flat white 3.60" >> prices.txt
git reset --hard HEAD~1
cat prices.txt
```

## Troubleshoot

```bash
git reflog -3
```

## Fix

```bash
git reset --hard ORIG_HEAD
git log --oneline -2
```

## Practice challenge

```bash
cd ~/git-practice/lesson-31
git reset --mixed HEAD~1
git status --short
git diff --stat
git reset -q --hard ORIG_HEAD
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-31
```
