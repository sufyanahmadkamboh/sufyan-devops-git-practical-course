<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 66 · Continuing a rebase · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-66 history
cd ~/git-practice/lesson-66
git log --oneline -4
```

## Demonstration

```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/edit/'" git rebase -i HEAD~4 2>&1
git status | head -4
```

```bash
echo "Now serving green tea." >> README.md
git commit -q --amend --no-edit -a
git show --stat --format=%s HEAD | tail -3
```

```bash
git rebase --continue
git log --oneline -4
git log --oneline -1 -- README.md
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-66
git log --oneline -6 --reverse
```

## Break it

```bash
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~2
sed -i 's/^mocha$/mocha (seasonal)/' menu.txt
git commit -q -am "Mark mocha as seasonal"
git rebase --continue
git log --oneline -3
```

## Fix

```bash
GIT_SEQUENCE_EDITOR="sed -i '2s/^pick/fixup/'" git rebase -q -i HEAD~3
git log --oneline -3
git show HEAD~1 | grep "^+mocha"
```

## Practice challenge

```bash
cd ~/git-practice/lesson-66
GIT_SEQUENCE_EDITOR="sed -i '1s/^pick/edit/'" git rebase -q -i HEAD~3
GIT_EDITOR="sed -i '/Price mocha/s/^pick/drop/'" git rebase --edit-todo
git rebase --continue > /dev/null
git log --oneline -3
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-66
```
