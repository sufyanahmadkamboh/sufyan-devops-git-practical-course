<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 14 · git show · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-14 history
cd ~/git-practice/lesson-14
git log --oneline
```

## Demonstration

```bash
git show
```

```bash
git show --stat HEAD~3
```

```bash
git show HEAD~3:prices.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-14
git show -s --format='%h %an %ad %s' "$(git log --format=%h --grep='Price green tea')"
```

## Break it

```bash
git show HEAD~4:hours.txt 2>&1
```

## Troubleshoot

```bash
git show --name-only --format= HEAD~4
git ls-tree --name-only HEAD~4
```

## Fix

```bash
git show HEAD~4:menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-14
git diff --name-only HEAD~3 HEAD
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-14
```
