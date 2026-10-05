<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 24 · Fast-forward merge · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-24 feature
cd ~/git-practice/lesson-24
git log --oneline --graph --all
```

## Demonstration

```bash
git merge feature-tea
git log --oneline --graph --all
```

```bash
git switch -q -c feature-hours && echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add hours"
git switch -q main
git merge --no-ff --no-edit feature-hours
git log --oneline --graph -4
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-24
git log --oneline -1
git log --oneline --merges | wc -l
```

## Break it

```bash
git switch -q -c feature-mocha HEAD~1 && echo "mocha 3.90" >> prices.txt && git commit -q -am "Price mocha"
git switch -q main
git merge --ff-only feature-mocha 2>&1
```

## Troubleshoot

```bash
git log --oneline --graph main feature-mocha | head -5
```

## Fix

```bash
git switch -q feature-mocha
git rebase -q main
git switch -q main
git merge --ff-only feature-mocha
```

## Practice challenge

```bash
cd ~/git-practice/lesson-24
git reset -q --hard ORIG_HEAD
git log --oneline --graph -3 main feature-mocha
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-24
```
