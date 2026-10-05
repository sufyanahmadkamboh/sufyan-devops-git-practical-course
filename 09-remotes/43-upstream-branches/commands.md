<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 43 · Upstream branches · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-43 remote
cd ~/git-practice/lesson-43/ada
```

## Demonstration

```bash
git branch -vv
```

```bash
git switch -q -c feature-chai && echo "chai" >> menu.txt && git commit -q -am "Add chai"
git push -u origin feature-chai
git branch -vv
```

```bash
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git status | head -2
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-43/ada
git log --oneline '@{u}..'
```

## Break it

```bash
git switch -q -c feature-mocha && echo "mocha" >> menu.txt && git commit -q -am "Add mocha"
git push 2>&1
```

## Fix

```bash
git push -q -u origin feature-mocha
git branch -vv | grep feature-mocha
```

## Practice challenge

```bash
cd ~/git-practice/lesson-43/ada
git switch -q -c hotfix origin/main
git branch -vv | grep hotfix
git push -q -u origin hotfix
git branch -vv | grep hotfix
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-43
```
