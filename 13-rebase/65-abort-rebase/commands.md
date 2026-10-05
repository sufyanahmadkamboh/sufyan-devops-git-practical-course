<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 65 · Aborting a rebase · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-65 conflict
cd ~/git-practice/lesson-65
git switch -q feature-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git rev-parse --short HEAD
```

## Demonstration

```bash
git rebase main 2>&1 | grep -E "CONFLICT|error"
test "${PIPESTATUS[0]}" -eq 0
```

```bash
git rebase --abort
git status
git log --oneline -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-65
grep latte prices.txt
```

## Break it

```bash
git rebase main > /dev/null 2>&1 || true
git rebase main 2>&1
```

## Troubleshoot

```bash
git status | head -3
```

## Fix

```bash
git rebase --abort
git status
```

## Practice challenge

```bash
cd ~/git-practice/lesson-65
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
grep latte prices.txt
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-65
```
