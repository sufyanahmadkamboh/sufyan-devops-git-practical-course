<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 77 · Branches are references · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-77 feature
cd ~/git-practice/lesson-77
```

## Demonstration

```bash
git for-each-ref --format='%(refname) -> %(objectname:short)'
cat .git/refs/heads/feature-tea 2> /dev/null || grep feature-tea .git/packed-refs
```

```bash
git update-ref refs/heads/experiment fc345e6
git branch -v
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-77
git branch --points-at main
```

## Break it

```bash
git update-ref -d refs/heads/feature-tea
git branch
git log --oneline --all | head -3
```

## Troubleshoot

```bash
git cat-file -p bb67674 | tail -1
```

## Fix

```bash
git branch feature-tea bb67674
git log --oneline -1 feature-tea
```

## Practice challenge

```bash
cd ~/git-practice/lesson-77
git update-ref refs/review/42 feature-tea
git for-each-ref refs/review
git branch | grep -c review || true
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-77
```
