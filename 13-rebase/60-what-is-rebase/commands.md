<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 60 · What is rebase? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-60 diverged
cd ~/git-practice/lesson-60
git log --oneline --graph --all
```

## Demonstration

```bash
before=$(git rev-parse --short feature-tea)
git switch -q feature-tea
git rebase main
echo "feature-tea was $before, is now $(git rev-parse --short HEAD)"
```

```bash
git log --oneline --graph --all
```

```bash
git reflog -4
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-60
git show 'feature-tea@{1}' | git patch-id | cut -c1-12
git show feature-tea | git patch-id | cut -c1-12
```

## Break it

```bash
git init -q --bare ../lesson-60-server.git && git remote add origin ../lesson-60-server.git
git push -q -u origin main feature-tea
git switch -q main && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Raise the espresso price" && git push -q
git switch -q feature-tea && git rebase -q main
git push 2>&1
```

## Fix

```bash
git push --force-with-lease 2>&1
```

## Practice challenge

```bash
cd ~/git-practice/lesson-60
git rebase -q --onto 4267004 main feature-tea
git log --oneline --graph -3
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-60 ~/git-practice/lesson-60-server.git
```
