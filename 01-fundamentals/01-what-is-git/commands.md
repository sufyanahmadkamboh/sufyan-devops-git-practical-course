<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 01 · What is Git? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
mkdir -p ~/git-practice/lesson-01/without-git
cd ~/git-practice/lesson-01
pwd
```

## Demonstration

```bash
cd without-git
printf 'espresso 2.50\nlatte 3.20\n' > prices-final.txt
cp prices-final.txt prices-final2.txt && printf 'cappuccino 3.40\n' >> prices-final2.txt
cp prices-final2.txt prices-final-final.txt && sed -i 's/latte 3.20/latte 3.30/' prices-final-final.txt
ls
```

```bash
cd ~/git-practice/lesson-01
mkdir with-git && cd with-git
git init -q -b main
git config user.name "Ada Lovelace" && git config user.email "ada@example.com"
printf 'espresso 2.50\nlatte 3.20\n' > prices.txt
git add prices.txt && git commit -q -m "Add prices"
printf 'cappuccino 3.40\n' >> prices.txt
git add prices.txt && git commit -q -m "Add cappuccino"
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add prices.txt && git commit -q -m "Raise the latte price"
git log --oneline
```

```bash
git show --stat --format='%h %an %ad%n%s' --date=short HEAD
git diff HEAD~1 HEAD
```

```bash
git show HEAD~2:prices.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-01/with-git
git log --oneline | head -1
git log --oneline | wc -l
```

## Break it

```bash
cd ~/git-practice/lesson-01/with-git
rm prices.txt
ls; git status --short; echo "(prices.txt deleted)"
```

## Fix

```bash
git restore prices.txt
cat prices.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-01/with-git
first=$(git rev-list --max-parents=0 HEAD)
git show "$first":prices.txt
git diff "$first" HEAD
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-01
```
