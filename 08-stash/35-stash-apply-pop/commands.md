<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 35 · Stash, apply and pop · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-35 feature
cd ~/git-practice/lesson-35
```

## Demonstration

```bash
sed -i 's/latte 3.20/latte 3.40/' prices.txt
git stash push -m "autumn prices"
git stash list
```

```bash
git stash apply -q
git commit -q -am "Autumn latte price on main"
git switch -q feature-tea
git stash apply -q
git diff --stat
git stash list
```

```bash
git commit -q -am "Autumn latte price on feature-tea"
git stash drop
git stash list | wc -l
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-35
git status --short
git stash show --name-only
```

## Break it

```bash
git commit -q -am "Espresso 2.60"
sed -i 's/^green tea$/green tea (sencha)/' menu.txt && git commit -q -am "Sencha"
git stash pop 2>&1
```

## Troubleshoot

```bash
git status --short
git stash list
```

## Fix

```bash
printf 'espresso\nlatte\ncappuccino\ngreen tea (sencha)\nchai\n' > menu.txt
git restore --staged menu.txt
git stash drop
cat menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-35
git stash -q
echo "mocha" >> menu.txt && git add menu.txt
sed -i 's/latte 3.40/latte 3.50/' prices.txt
git stash -q
git stash pop -q --index
git status --short
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-35
```
