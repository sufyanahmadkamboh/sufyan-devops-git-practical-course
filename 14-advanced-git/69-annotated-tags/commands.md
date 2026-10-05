<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 69 · Annotated tags · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-69 history
cd ~/git-practice/lesson-69
git tag v0.9.0 fc345e6
```

## Demonstration

```bash
git tag -a v1.0.0 4267004 -m "Release 1.0.0: the first menu with prices"
git show v1.0.0 --stat | head -8
```

```bash
for t in v0.9.0 v1.0.0; do echo "$t $(git cat-file -t "$t")"; done
git tag -n
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-69
git describe
```

## Break it

```bash
git tag -d v1.0.0 > /dev/null
git describe 2>&1
```

## Fix

```bash
git tag -a v1.0.0 4267004 -m "Release 1.0.0"
git describe
git describe --tags --abbrev=0 HEAD~4
```

## Practice challenge

```bash
cd ~/git-practice/lesson-69
git for-each-ref refs/tags/v1.0.0 --format='%(taggername) %(taggerdate:short)'
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-69
```
