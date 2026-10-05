<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 64 · Rebase conflicts · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-64 conflict
cd ~/git-practice/lesson-64
git switch -q feature-tea
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --graph --all
```

## Demonstration

```bash
git rebase main 2>&1 | grep -v "^hint:"
test "${PIPESTATUS[0]}" -eq 0
```

```bash
git status
```

```bash
cat prices.txt
```

```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git rebase --continue
git log --oneline --graph -4
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-64
git log -2 --format='%s by %an'
```

## Break it

```bash
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git rebase --continue 2>&1
```

## Troubleshoot

```bash
git status --short
git status | grep "both modified"
```

## Fix

```bash
git add prices.txt
git rebase --continue
```

## Practice challenge

```bash
cd ~/git-practice/lesson-64
git config rerere.enabled true
git reset -q --hard ORIG_HEAD
git rebase main > /dev/null 2>&1 || true
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt && git add prices.txt && git rebase --continue > /dev/null
git reset -q --hard ORIG_HEAD
git rebase main 2>&1 | grep -i "resolved" || true
git rebase --abort
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-64
```
