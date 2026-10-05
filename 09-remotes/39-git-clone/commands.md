<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 39 · git clone · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-39 remote
cd ~/git-practice/lesson-39
(cd ada && git switch -q -c feature-tea && echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q -u origin feature-tea)
```

## Demonstration

```bash
git clone server/cafe.git linus
cd linus
git branch -a
git log --oneline --all
```

```bash
git switch feature-tea
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-39/shallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

## Break it

```bash
cd ~/git-practice/lesson-39
git clone server/cafe.git ada 2>&1
```

## Troubleshoot

```bash
git -C ada remote -v
```

## Fix

```bash
git clone -q server/cafe.git ada-2
ls
```

## Practice challenge

```bash
cd ~/git-practice/lesson-39/shallow
git fetch -q --unshallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-39
```
