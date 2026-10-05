<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 17 · Why branches exist · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-17 basic        # one branch for everything
bash scripts/new-lab.sh lesson-17b basic       # the same project, with branches
cd ~/git-practice/lesson-17
```

## Demonstration

```bash
echo "loyalty card: 10th coffee free (WORK IN PROGRESS)" >> README.md
git commit -q -am "WIP: loyalty card"
git log --oneline
```

```bash
sed -i 's/latte 3.20/latte 3.10/' prices.txt
git commit -q -am "Fix the latte price"
git log --oneline -2
```

```bash
cd ~/git-practice/lesson-17b
git switch -q -c feature-loyalty
echo "loyalty card: 10th coffee free (WORK IN PROGRESS)" >> README.md
git commit -q -am "WIP: loyalty card"
git switch -q main
sed -i 's/latte 3.20/latte 3.10/' prices.txt
git commit -q -am "Fix the latte price"
git log --oneline --graph --all
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-17b
git log --oneline main..feature-loyalty
```

## Break it

```bash
cd ~/git-practice/lesson-17
git log --oneline main
```

## Fix

```bash
cd ~/git-practice/lesson-17
fix=$(git rev-parse HEAD)                    # remember the fix commit (the latest one)
git branch feature-loyalty HEAD~1            # a branch that keeps the WIP commit
git reset -q --hard HEAD~2                   # main back to before the WIP (lesson 31)
git cherry-pick "$fix" > /dev/null           # copy only the fix onto main
git log --oneline main
```

## Practice challenge

```bash
cd ~/git-practice/lesson-17b
git switch -q -c feature-a main && echo a > a.txt && git add a.txt && git commit -q -m "Feature A"
git switch -q -c feature-b main && echo b > b.txt && git add b.txt && git commit -q -m "Feature B"
git log --oneline --graph feature-a feature-b main
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-17 ~/git-practice/lesson-17b
```
