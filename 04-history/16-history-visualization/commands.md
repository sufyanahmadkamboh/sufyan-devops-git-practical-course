<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 16 · Commit history visualization · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-16 diverged
cd ~/git-practice/lesson-16
```

## Demonstration

```bash
git log --oneline --graph --all
```

```bash
git merge -q --no-edit feature-tea
git log --oneline --graph --all
```

```bash
git log --format='%h  parents: %p  %s' -5
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-16
git log --oneline --first-parent
```

## Break it

```bash
git switch -q feature-tea
git log --oneline --graph
```

## Fix

```bash
git log --oneline --graph --all
git switch -q main
```

## Practice challenge

```bash
cd ~/git-practice/lesson-16
git rev-list --left-right --count main...feature-tea
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-16
```
