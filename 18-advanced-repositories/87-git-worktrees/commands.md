<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 87 · Git worktrees · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-87 feature
cd ~/git-practice/lesson-87
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt
git status --short
```

## Demonstration

```bash
git worktree add -b hotfix ../lesson-87-hotfix main
git worktree list
```

```bash
cd ../lesson-87-hotfix
sed -i 's/espresso 2.50/espresso 2.40/' prices.txt && git commit -q -am "Fix the espresso price"
git log --oneline -1
```

```bash
cd ../lesson-87
git status --short
git log --oneline -1 hotfix
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-87
git log --oneline -1 main
```

## Break it

```bash
git switch main 2>&1
```

## Fix

```bash
git stash -q
git worktree remove ../lesson-87-hotfix
git worktree list
git switch -q main && git branch --show-current
git switch -q feature-tea && git stash pop -q
```

## Practice challenge

```bash
cd ~/git-practice/lesson-87
git worktree add -q --detach ../lesson-87-review main
rm -rf ../lesson-87-review
git worktree prune
git worktree list
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-87 ~/git-practice/lesson-87-hotfix ~/git-practice/lesson-87-review
```
