<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 32 · git revert · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-32 history
cd ~/git-practice/lesson-32
git log --oneline
```

## Demonstration

```bash
target=$(git log --format=%h --grep="^Add mocha")
git revert --no-edit "$target"
git log --oneline -3
```

```bash
git show --format='%s%n%b' HEAD
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-32
grep mocha menu.txt
git log --oneline -2
```

## Break it

```bash
sed -i 's/^green tea$/green tea (organic)/' menu.txt && git commit -q -am "Organic green tea"
git revert --no-edit "$(git log --format=%h --grep='^Add green tea')" 2>&1
```

## Troubleshoot

```bash
git status | head -4
```

## Fix

```bash
grep -v -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>' -e 'green tea' -e '^|||||||' menu.txt > menu.tmp && mv menu.tmp menu.txt
git add menu.txt
git revert --continue > /dev/null
cat menu.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-32
git revert --no-commit HEAD~1..HEAD
git commit -q -m "Revert the last two commits"
git log --oneline -1
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-32
```
