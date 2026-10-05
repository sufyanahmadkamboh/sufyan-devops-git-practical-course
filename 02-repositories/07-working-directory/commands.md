<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 07 · The working directory · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-07 basic
cd ~/git-practice/lesson-07
```

## Demonstration

```bash
git status
```

```bash
echo "green tea" >> menu.txt                 # modify a tracked file
rm prices.txt                                # delete a tracked file
echo "Open 8-18" > hours.txt                 # create a new file
git status
```

```bash
git diff menu.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-07
git status --short
```

## Break it

```bash
git restore menu.text 2>&1
```

## Troubleshoot

```bash
git ls-files
```

## Fix

```bash
git restore menu.txt prices.txt
git add -A && git status --short
```

## Practice challenge

```bash
cd ~/git-practice/lesson-07
git restore --staged . && git restore . && rm -f INFO.md hours.txt && git checkout -q -- README.md 2>/dev/null; git status --short
echo "chai" >> menu.txt
echo "Monday: 2 for 1" > specials.txt
git status --short
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-07
```
