<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 22 · Deleting branches · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-22 feature
cd ~/git-practice/lesson-22
git switch -q -c experiment && echo "oat milk" >> menu.txt && git commit -q -am "Try oat milk" && git switch -q main
git log --oneline --graph --all
```

## Demonstration

```bash
git merge -q feature-tea
git branch --merged
git branch -d feature-tea
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-22
git branch --no-merged
```

## Break it

```bash
git branch -d experiment 2>&1
```

## Troubleshoot

```bash
git log --oneline main..experiment
```

## Fix

```bash
git rev-parse --short experiment
git branch -D experiment
```

## Practice challenge

```bash
cd ~/git-practice/lesson-22
git branch done-1 && git branch done-2
git branch --merged main | grep -vE '^\*|^\s*main$' | xargs -r git branch -d
git branch
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-22
```
