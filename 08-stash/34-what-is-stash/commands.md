<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 34 · What is a stash? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-34 basic
cd ~/git-practice/lesson-34
```

## Demonstration

```bash
echo "flat white" >> menu.txt
echo "flat white 3.60" >> prices.txt
git status --short
```

```bash
git stash
git stash list
git status
```

```bash
sed -i 's/espresso 2.50/espresso 2.40/' prices.txt
git commit -q -am "Fix the espresso price"
git log --oneline -1
```

```bash
git stash pop
cat prices.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-34
grep "flat white" menu.txt
git stash list | wc -l
```

## Break it

```bash
echo "Monday: free cookie" > specials.txt
git stash
git status --short
```

## Fix

```bash
git stash pop -q
git stash -u
git status
git stash pop -q
```

## Practice challenge

```bash
cd ~/git-practice/lesson-34
git stash -q
git show-ref | grep stash
git log --oneline -1 stash
git stash pop -q
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-34
```
