<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 78 · Detached HEAD · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-78 history
cd ~/git-practice/lesson-78
git tag v1.0.0 4267004
```

## Demonstration

```bash
git switch --detach v1.0.0
```

```bash
git status | head -2
cat .git/HEAD
git branch
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-78
cat menu.txt
```

## Break it

```bash
sed -i 's/espresso 2.50/espresso 2.45/' prices.txt && git commit -q -am "Hotfix: espresso price"
git switch main 2>&1
```

## Troubleshoot

```bash
git reflog | grep -m1 "Hotfix"
```

## Fix

```bash
git branch hotfix-espresso "$(git reflog --format=%h --grep-reflog='commit: Hotfix' | head -1)"
git log --oneline -1 hotfix-espresso
```

## Practice challenge

```bash
cd ~/git-practice/lesson-78
git switch -q --detach HEAD~2
echo "idea" > idea.txt && git add idea.txt && git commit -q -m "Try an idea"
git switch -c experiment
git status | head -1
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-78
```
