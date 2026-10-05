<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 10 · The staging area · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-10 basic
cd ~/git-practice/lesson-10
```

## Demonstration

```bash
sed -i 's/small cafe/small, friendly cafe/' README.md
echo "green tea" >> menu.txt
git status --short
```

```bash
git add README.md
echo "=== git diff (working directory vs staging area: NOT staged)"
git diff
echo "=== git diff --staged (staging area vs last commit: WILL be committed)"
git diff --staged
```

```bash
git commit -q -m "Describe the cafe"
git add menu.txt && git commit -q -m "Add green tea"
git log --oneline -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-10
git diff --staged | grep '^[+-][a-z]'
git diff | grep '^[+-][a-z]'
```

## Break it

```bash
git commit -q -m "Update espresso price and add chai"
git status --short
```

## Troubleshoot

```bash
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

## Fix

```bash
git add menu.txt
git commit -q --amend --no-edit
git show --format='%s' HEAD | grep '^[+-][a-z]'
```

## Practice challenge

```bash
cd ~/git-practice/lesson-10
printf 'ristretto\nlatte\ncappuccino\ngreen tea\nchai\nmocha\n' > menu.txt
git diff
# git add -p asks about each hunk. Both edits are close together, so Git shows them as ONE hunk:
# "s" splits it, then "y" stages the first part and "n" skips the second.
printf 's\ny\nn\n' | git add -p menu.txt > /dev/null
git commit -q -m "Rename espresso to ristretto"
git add menu.txt && git commit -q -m "Add mocha"
git log --oneline -2
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-10
```
