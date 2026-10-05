<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 20 · Create and switch in one command · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-20 diverged
cd ~/git-practice/lesson-20
```

## Demonstration

```bash
git switch -c feature-login
git branch
```

```bash
git switch -c fix-tea-price feature-tea
git log --oneline -1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-20
git log --oneline main..feature-hours
```

## Break it

```bash
git switch -q fix-tea-price
git switch -c feature-specials
echo "Monday special" > specials.txt && git add specials.txt && git commit -q -m "Add specials"
git log --oneline main..feature-specials
```

## Fix

```bash
git rebase -q --onto main fix-tea-price feature-specials
git log --oneline main..feature-specials
```

## Practice challenge

```bash
cd ~/git-practice/lesson-20
git switch -c release-test main~2
git log --oneline -1
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-20
```
