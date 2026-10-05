<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 33 · git reflog · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-33 history
cd ~/git-practice/lesson-33
```

## Demonstration

```bash
git reset -q --hard HEAD~3
git log --oneline
```

```bash
git reflog
```

```bash
git reset --hard 'HEAD@{1}'
git log --oneline -2
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-33
git reflog show main | head -3
git log --oneline -1 rescue
```

## Break it

```bash
git switch -q -c risky && echo "seasonal: pumpkin latte" >> menu.txt && git commit -q -am "Add pumpkin latte"
git switch -q main
git branch -D risky
```

## Troubleshoot

```bash
git reflog | grep -m1 "pumpkin"
```

## Fix

```bash
lost=$(git reflog --format=%h --grep-reflog="commit: Add pumpkin latte" | head -1)
git branch risky "$lost"
git log --oneline -1 risky
```

## Practice challenge

```bash
cd ~/git-practice/lesson-33
git reflog show --date=relative main | head -3 | sed -E 's/[0-9]+ (seconds?|minutes?) ago/N seconds ago/'
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-33
```
