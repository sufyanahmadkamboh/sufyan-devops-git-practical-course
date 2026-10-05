<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 63 · Interactive rebase · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-63 history
cd ~/git-practice/lesson-63
git log --oneline
```

## Demonstration

```bash
GIT_SEQUENCE_EDITOR=cat git rebase -i HEAD~4
```

```bash
GIT_SEQUENCE_EDITOR="sed -i -e '2s/^pick/squash/' -e '4s/^pick/fixup/'" git rebase -q -i HEAD~4
git log --oneline -3
git show --stat --format='%s%n%b' HEAD~1
```

```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/reword/'" GIT_EDITOR="sed -i '1s/.*/Add mocha with its price/'" git rebase -q -i HEAD~2
git log --oneline -3
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-63
cat menu.txt prices.txt
git log --oneline -2
```

## Break it

```bash
echo "chai" >> menu.txt && git commit -q -am "WIP chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "fix: forgot the price"
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/squash/'" git rebase -i HEAD~1 2>&1
```

## Troubleshoot

```bash
git status | head -2
git rebase --abort 2>&1 || true
```

## Fix

```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/fixup/'" git rebase -q -i HEAD~2
git commit -q --amend -m "Add chai with its price"
git log --oneline -3
git show --stat --format=%s HEAD | tail -3
```

## Practice challenge

```bash
cd ~/git-practice/lesson-63
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt
git commit -q -a --fixup=4267004
git log --oneline -1
GIT_SEQUENCE_EDITOR=true git rebase -q -i --autosquash fc345e6
git log --oneline
git show ':/^Add prices' | grep "^+espresso"
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-63
```
