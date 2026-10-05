<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 08 · git status · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-08 remote
cd ~/git-practice/lesson-08/ada
```

## Demonstration

```bash
git status
```

```bash
echo "green tea" >> menu.txt && git add menu.txt && git commit -q -m "Add green tea"
echo "chai" >> menu.txt && git add menu.txt          # staged
sed -i 's/latte 3.20/latte 3.30/' prices.txt         # modified, not staged
echo "Open 8-18" > hours.txt                         # untracked
git status
```

```bash
git status --short --branch
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-08/ada
git status --short
```

## Break it

```bash
git commit -q -m "Add chai"
git status --short
```

## Troubleshoot

```bash
git show --stat --format='%s' HEAD
git show HEAD | grep '^[+-][^+-]'
```

## Fix

```bash
git add prices.txt menu.txt && git commit -q -m "Raise the latte price, add matcha"
rm hours.txt
git status
```

## Practice challenge

```bash
cd ~/git-practice/lesson-08/ada
echo "2 for 1" > specials.txt && git add specials.txt
rm README.md
echo "todo" > notes.txt
git status --short
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-08
```
