<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 13 · git log · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-13 history
cd ~/git-practice/lesson-13
```

## Demonstration

```bash
git log -2
```

```bash
git log --oneline
```

```bash
git switch -q -c feature-tea HEAD~2
echo "matcha" >> menu.txt && git commit -q -am "Add matcha"
git switch -q main
git log --oneline --graph --all
```

```bash
echo "--- commits that changed prices.txt"
git log --oneline -- prices.txt
echo "--- commits whose message mentions mocha"
git log --oneline --grep=mocha
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-13
git log --oneline main..feature-tea
```

## Break it

```bash
git log --oneline --grep=matcha
```

## Troubleshoot

```bash
git status | head -1
git branch
```

## Fix

```bash
git log --oneline --all --grep=matcha
git branch --contains "$(git log --all --format=%h --grep=matcha)"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-13
git log --format='%h | %an | %ar | %s' -- menu.txt
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-13
```
