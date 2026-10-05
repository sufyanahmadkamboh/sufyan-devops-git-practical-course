<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 29 · Undo working directory changes · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-29 basic
cd ~/git-practice/lesson-29
```

## Demonstration

```bash
sed -i 's/2.50/25.00/' prices.txt
echo "free cookies" >> menu.txt
git status --short
```

```bash
git restore prices.txt
git status --short
head -1 prices.txt
```

```bash
git restore .
git status
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-29
git restore --source=4267004 prices.txt
cat prices.txt
```

## Break it

```bash
printf 'flat white\ncortado\n' >> menu.txt
git restore menu.txt
cat menu.txt
```

## Troubleshoot

```bash
git reflog | head -3
git stash list
git fsck --lost-found 2>/dev/null | head -3 || true
```

## Fix

```bash
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
echo "a bad experiment" >> menu.txt
git restore menu.txt
cat menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-29
git restore --source=HEAD --staged --worktree .
sed -i 's/espresso 2.50/espresso 2.60/; s/cappuccino 3.40/cappuccino 9.99/' prices.txt
printf 's\nn\ny\n' | git restore -p prices.txt > /dev/null
cat prices.txt
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-29
```
