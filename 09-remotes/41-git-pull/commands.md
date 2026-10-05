<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 41 · git pull · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-41 remote
cd ~/git-practice/lesson-41/grace
echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q
cd ../ada
```

## Demonstration

```bash
git pull
git log --oneline -2
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-41/ada
git pull --ff-only
git log --oneline -1
```

## Break it

```bash
cd ~/git-practice/lesson-41/grace && echo "mocha" >> menu.txt && git commit -q -am "Add mocha" && git push -q
cd ../ada && sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "Espresso 2.60"
git pull 2>&1
```

## Troubleshoot

```bash
git status | head -3
```

## Fix

```bash
git pull --no-rebase --no-edit
git log --oneline --graph -4
```

```bash
git reset -q --hard HEAD~1
git pull --rebase
git log --oneline --graph -3
```

## Practice challenge

```bash
cd ~/git-practice/lesson-41/ada
git config pull.rebase true
git config rebase.autoStash true
git config --get pull.rebase && git config --get rebase.autoStash
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-41
```
