<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 15 · git diff · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-15 diverged
cd ~/git-practice/lesson-15
```

## Demonstration

```bash
sed -i 's/latte 3.20/latte 3.30/' prices.txt
echo "chai" >> menu.txt && git add menu.txt
echo "=== git diff          (working directory vs staging area)"; git diff
echo "=== git diff --staged (staging area vs HEAD)";                git diff --staged
echo "=== git diff HEAD     (working directory vs HEAD)";           git diff HEAD --stat
```

```bash
echo "=== HEAD~2 vs HEAD";             git diff HEAD~2 HEAD --stat
echo "=== main vs feature-tea";        git diff main feature-tea
echo "=== since feature-tea branched"; git diff main...feature-tea --stat
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-15
git diff --word-diff prices.txt
```

## Break it

```bash
git diff main..featur-tea 2>&1
```

## Troubleshoot

```bash
git branch --all
```

## Fix

```bash
git diff main..feature-tea -- menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-15
git diff feature-tea -- README.md
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-15
```
