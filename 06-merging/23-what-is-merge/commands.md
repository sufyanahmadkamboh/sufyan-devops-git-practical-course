<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 23 · What is a merge? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-23 diverged
cd ~/git-practice/lesson-23
git log --oneline --graph --all
```

## Demonstration

```bash
git switch -q main
git merge --no-edit feature-tea
```

```bash
git log --oneline --graph --all
cat menu.txt README.md
```

```bash
git log -1 --format='%h parents: %p'
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-23
git log --oneline --merges
```

## Break it

```bash
git merge feature-tea
```

## Fix

```bash
git switch -q feature-tea
git merge main
git log --oneline -1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-23
git switch -q main
git switch -q -c a && echo a > a.txt && git add a.txt && git commit -q -m "Add a"
git switch -q main && git switch -q -c b && echo b > b.txt && git add b.txt && git commit -q -m "Add b"
git switch -q main
git merge -q --no-edit a
git merge -q --no-edit b
git log --oneline --graph -6
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-23
```
